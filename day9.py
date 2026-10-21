import json, os, uuid
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

class ChatRequest(BaseModel):
    messages: List[dict]
    stream: bool = False
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512

# ---------- 会话版：服务端管理多轮历史（命令行版 ChatBot 搬进来） ----------
class ChatSession:
    """等价于命令行版 ChatBot，三个适配点：
    1. client 由同步 OpenAI 换成全局 AsyncOpenAI（调用处 await）
    2. print(t, end="") 换成 yield SSE（输出通道：终端 → HTTP 流）
    3. self.messages 换成 sessions[session_id].messages（单用户 → 按 id 隔离多用户）
    while True: input() 的 REPL 循环则由前端页面承担。
    """
    def __init__(self, system_prompt: str = "你是耐心的编程助教，回答简洁，使用中文。"):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.total_tokens = 0

sessions: Dict[str, ChatSession] = {}   # 内存版会话表：sid -> 会话（进程重启即丢）

def get_session(session_id: str) -> ChatSession:
    if session_id not in sessions:      # 首次见到该 id：新建会话（带 system prompt）
        sessions[session_id] = ChatSession()
    return sessions[session_id]

class BotRequest(BaseModel):
    message: str                        # 本轮用户提问（历史由服务端管，前端不用传 messages）
    session_id: Optional[str] = None    # 不传则由服务端分配
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512

# ---------- 普通版：一次性返回 ----------
@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        resp = await client.chat.completions.create(
            model="deepseek-chat", messages=req.messages,
            temperature=req.temperature, max_tokens=req.max_tokens, stream=False,
        )
    except Exception as e:
        raise HTTPException(502, f"upstream error: {e}")
    return {
        "reply": resp.choices[0].message.content,
        "finish_reason": resp.choices[0].finish_reason,
        "usage": resp.usage.model_dump() if resp.usage else None,
    }

# ---------- 流式版：SSE ----------
@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    async def event_gen():
        try:
            stream = await client.chat.completions.create(
                model="deepseek-chat", messages=req.messages,
                temperature=req.temperature, max_tokens=req.max_tokens,
                stream=True, stream_options={"include_usage": True},
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    payload = {"content": chunk.choices[0].delta.content}
                    # ensure_ascii=False：否则中文变成 \uXXXX
                    yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
                if chunk.usage:
                    yield f"data: {json.dumps({'usage': chunk.usage.model_dump()}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)[:200]}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",   # 关 Nginx 缓冲，关键
        },
    )

# ---------- 会话版：服务端管历史，前端只发一句话 ----------
@app.post("/api/bot/stream")
async def bot_stream(req: BotRequest):
    sid = req.session_id or str(uuid.uuid4())
    bot = get_session(sid)
    bot.messages.append({"role": "user", "content": req.message})   # 追加本轮提问

    async def event_gen():
        reply, usage = [], None
        try:
            stream = await client.chat.completions.create(
                model="deepseek-chat", messages=bot.messages,
                temperature=req.temperature, max_tokens=req.max_tokens,
                stream=True, stream_options={"include_usage": True},
            )
            # 首条事件：告知前端分配的会话 id
            yield f"data: {json.dumps({'session_id': sid}, ensure_ascii=False)}\n\n"
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    t = chunk.choices[0].delta.content
                    reply.append(t)   # 攒完整回复，流结束后回填历史
                    yield f"data: {json.dumps({'content': t}, ensure_ascii=False)}\n\n"
                if chunk.usage:
                    usage = chunk.usage
            # 回填历史：等价于 ChatBot.ask 里的 append assistant 消息
            if reply:
                bot.messages.append({"role": "assistant", "content": "".join(reply)})
            if usage:
                bot.total_tokens += usage.total_tokens
                yield f"data: {json.dumps({'usage': usage.model_dump(), 'total_tokens': bot.total_tokens}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)[:200]}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

# ---------- 首页：直接托管聊天页面 ----------
@app.get("/")
async def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))