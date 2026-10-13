x = 10
print(type(x))
print(x)

x = "hello"
print(type(x))

print(isinstance(x, str))

#name = input("请输入姓名：")
#print(f"hello {name}")
#score = input("请输入成绩：")
#score = int(score)
#print(f"成绩是：{score}")
for i in range(0,5,1):
    print(i)
for i, name in enumerate(["Tom", "Jerry"], start=1):
    print(i, name)

def greet(name, prefix="Hello"):
    return f"{prefix}, {name}"

print(greet("Tom"))
print(greet("Tom", prefix="Hi"))