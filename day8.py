import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

messages = [
    {"role": "system", "content": "你是一位耐心的编程助教，回答简洁，使用中文。"},
    {"role": "user", "content": "用一句话解释什么是 token。"},
]

resp = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    stream=False,
    temperature=0.2,
    # 旧参数（思考模式，已由 temperature=0.2 方案替换）：
    # reasoning_effort="low",
    # extra_body={"thinking": {"type": "enabled"}},
    max_tokens=4096,
)

print("回复：", resp.choices[0].message.content)


u = resp.usage
print("输入 token:", u.prompt_tokens)
print("输出 token:", u.completion_tokens)
print("总 token:", u.total_tokens)

# ---- 第二轮：把上一轮的问答拼回 messages，实现多轮对话 ----
messages.append({"role": "assistant", "content": resp.choices[0].message.content})
messages.append({"role": "user", "content": "那上下文窗口又是什么？"})
resp2 = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    stream=False,
    temperature=0.2,
    # 旧参数（思考模式，已由 temperature=0.2 方案替换）：
    # reasoning_effort="low",
    # extra_body={"thinking": {"type": "enabled"}},
    max_tokens=4096,
)
print("回复2：", resp2.choices[0].message.content)
print("第二次输入 token:", resp2.usage.prompt_tokens)   # 会比第一次明显变大
