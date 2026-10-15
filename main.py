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

def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([3, 1, 9])
print(low, high)

def summarize(nums):
    """返回列表的最大值、最小值、平均值"""
    if not nums:
        raise ValueError("列表不能为空")
    return max(nums), min(nums), sum(nums) / len(nums)

def main(score_input=None):
    # 如果没有传入参数，则从控制台读取
    if score_input is None:
        score = input("请输入成绩：")
    else:
        score = score_input
    
    score = int(score)
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 60:
        print("C")
    else:
        print("D")

def add_student(name, scores):

if __name__ == "__main__":
    hi, lo, avg = summarize([88, 92, 75, 61, 100])
    print(f"最大值: {hi}, 最小值: {lo}, 平均值: {avg:.2f}")

