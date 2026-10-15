"""day4 练习：列表去重、单词计数、字典存学生平均分、set 求共同元素"""

from collections import Counter    # Counter 是专门用来计数的字典子类


# ===== 练习1：列表去重（保持原有顺序）=====
def dedup(items):
    result = []                       # 准备一个空列表，用来存放"没见过"的元素
    for item in items:                # 逐个取出原列表中的元素
        if item not in result:        # 检查 result 里是否已经有它（没有才往下走）
            result.append(item)       # 第一次出现的元素加入 result，之后重复的会被 if 挡住
    return result                     # 返回去重后的新列表，原列表不受影响


# ===== 练习2：统计一段文字中每个单词出现次数 =====
def word_count(text):
    counts = {}                       # 空字典，结构是 {单词: 出现次数}
    for word in text.split():         # split() 按空白字符切分文字，得到单词列表，逐个遍历
        counts[word] = counts.get(word, 0) + 1
        # counts.get(word, 0)：取出该单词已记录的次数；若字典里还没有这个键，返回默认值 0
        # 然后把次数 +1 重新写回字典——第一次遇到就是 0+1=1，之后不断累加
    return counts


# 扩展写法：用标准库 collections.Counter 一行完成计数
def word_count_counter(text):
    return Counter(text.split())      # 直接把单词列表交给 Counter，它自动统计每个元素出现的次数
                                      # 结果就是字典（支持 counts["the"]、counts.get(...) 等字典操作）
                                      # 还有额外好处：.most_common(3) 能直接取出出现最多的前 3 个单词


# ===== 练习3：用字典存 3 个学生，打印每个学生平均分 =====
students = {
    "Tom": [88, 92, 75],      # 键是学生姓名，值是成绩列表
    "Jerry": [61, 70, 80],
    "Spike": [90, 85, 95],
}


# ===== 练习4：用 set 找出两个列表的共同元素 =====
def common_items(list1, list2):
    # set(list1) & set(list2)：把两个列表各转成集合，& 取"交集"（两边的共同元素）
    # 集合交集会自动去重，最后用 list() 转回列表方便打印
    return list(set(list1) & set(list2))


if __name__ == "__main__":
    print(dedup([1, 2, 2, 3, 3, 3, "a", "a"]))          # 练习1：[1, 2, 3, 'a']

    text = "the quick brown fox jumps over the lazy dog the fox"
    print(word_count(text))                             # 练习2：手写字典计数
    print(word_count_counter(text))                     # 练习2扩展：Counter 一行计数
    print(Counter(text.split()).most_common(2))         # Counter 附赠能力：出现最多的前 2 个单词

    for name, scores in students.items():               # items() 同时取出键和值，循环出 (姓名, 成绩列表)
        print(f"{name} 平均分: {sum(scores) / len(scores):.2f}")   # sum 求总分除以科目数，:.2f 保留两位小数

    print(common_items([1, 2, 3, 4], [3, 4, 5, 6]))     # 练习4：[3, 4]
