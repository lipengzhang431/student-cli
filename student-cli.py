def average(scores):
    return sum(scores) / len(scores) if scores else 0.0


def add_student(students):
    sid = input("请输入学号：").strip()
    if not sid:
        print("学号不能为空")
        return
    if sid in students:
        print("学号已存在")
        return

    name = input("请输入姓名：").strip()
    scores_text = input("请输入成绩，用逗号分隔：").strip()

    scores = []
    if scores_text:
        for item in scores_text.split(","):
            try:
                scores.append(float(item.strip()))
            except ValueError:
                print(f"成绩格式错误：{item}")
                return

    students[sid] = {"name": name, "scores": scores}
    print("添加成功")


def delete_student(students):
    sid = input("请输入要删除的学号：").strip()
    if students.pop(sid, None) is None:
        print("未找到该学生")
    else:
        print("删除成功")


def find_student(students):
    sid = input("请输入要查询的学号：").strip()
    student = students.get(sid)
    if student is None:
        print("未找到该学生")
        return

    avg = average(student["scores"])
    print(f"学号：{sid}")
    print(f"姓名：{student['name']}")
    print(f"成绩：{student['scores']}")
    print(f"平均分：{avg:.2f}")


def list_students(students):
    if not students:
        print("暂无学生")
        return

    for sid, student in students.items():
        avg = average(student["scores"])
        print(f"{sid}\t{student['name']}\t{student['scores']}\t平均：{avg:.2f}")


def show_averages(students):
    if not students:
        print("暂无学生")
        return

    for sid, student in students.items():
        avg = average(student["scores"])
        print(f"{sid} {student['name']} 平均分：{avg:.2f}")


def main():
    students = {}

    while True:
        print("\n=== 学生成绩管理 ===")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 查询学生")
        print("4. 列出全部")
        print("5. 查看平均分")
        print("0. 退出")

        choice = input("请选择：").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            delete_student(students)
        elif choice == "3":
            find_student(students)
        elif choice == "4":
            list_students(students)
        elif choice == "5":
            show_averages(students)
        elif choice == "0":
            print("再见")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()