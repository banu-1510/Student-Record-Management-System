
import json
import os

DATA_FILE = "students.json"
students = []


def load_students():
    global students

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list) and all(
                isinstance(s, dict)
                and all(k in s for k in ("id", "name", "age", "marks"))
                for s in data
            ):
                students = data
            else:
                print("Invalid student data format.")
                students = []

        except (json.JSONDecodeError, OSError):
            print("Could not read student data.")
            students = []


def save_students():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save student records.")
        return False


def display_menu():
    print("\n" + "=" * 45)
    print("   STUDENT RECORD MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Student Statistics Report")
    print("7. Exit")


def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


def display_student(student):
    print("\nStudent Details")
    print("-" * 30)
    print("Student ID :", student["id"])
    print("Name       :", student["name"])
    print("Age        :", student["age"])
    print("Marks      :", student["marks"])
    print("Grade      :", calculate_grade(student["marks"]))
    print("-" * 30)


def add_student():
    print("\n--- Add Student ---")
    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty!")
        return

    if any(s["id"].lower() == student_id.lower() for s in students):
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Student name cannot be empty!")
        return

    try:
        age = int(input("Enter Student Age: "))
        marks = float(input("Enter Student Marks (0-100): "))

        if age <= 0 or not 0 <= marks <= 100:
            print("Enter a valid age and marks between 0 and 100!")
            return

    except ValueError:
        print("Enter a whole number for age and a numeric mark.")
        return

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "marks": marks
    }

    students.append(student)

    if save_students():
        print("Student added and saved successfully!")
    else:
        students.remove(student)


def view_students():
    print("\n--- All Student Records ---")

    if not students:
        print("No student records found!")
        return

    print("-" * 70)
    print(f"{'ID':<12}{'Name':<20}{'Age':<8}{'Marks':<12}{'Grade':<10}")
    print("-" * 70)

    for student in students:
        print(
            f"{student['id']:<12}"
            f"{student['name']:<20}"
            f"{student['age']:<8}"
            f"{student['marks']:<12.2f}"
            f"{calculate_grade(student['marks']):<10}"
        )

    print("-" * 70)


def search_student():
    student_id = input("\nEnter Student ID to search: ").strip()

    for student in students:
        if student["id"].lower() == student_id.lower():
            display_student(student)
            return

    print("Student not found!")


def update_student():
    student_id = input("\nEnter Student ID to update: ").strip()

    for student in students:
        if student["id"].lower() == student_id.lower():
            display_student(student)
            print("Leave a field empty to keep its current value.")

            name = input("New name: ").strip()
            age_input = input("New age: ").strip()
            marks_input = input("New marks: ").strip()

            try:
                age = int(age_input) if age_input else student["age"]
                marks = float(marks_input) if marks_input else student["marks"]

                if age <= 0 or not 0 <= marks <= 100:
                    print("Invalid age or marks. Update cancelled!")
                    return

            except ValueError:
                print("Invalid numeric input. Update cancelled!")
                return

            old_student = student.copy()

            if name:
                student["name"] = name

            student["age"] = age
            student["marks"] = marks

            if save_students():
                print("Student updated successfully!")
            else:
                student.update(old_student)
                print("Update cancelled because saving failed.")

            return

    print("Student not found!")


def delete_student():
    student_id = input("\nEnter Student ID to delete: ").strip()

    for student in students:
        if student["id"].lower() == student_id.lower():
            display_student(student)
            confirm = input("Delete this record? (yes/no): ").strip().lower()

            if confirm == "yes":
                index = students.index(student)
                students.pop(index)

                if save_students():
                    print("Student deleted successfully!")
                else:
                    students.insert(index, student)
                    print("Deletion failed because saving failed.")
            else:
                print("Deletion cancelled!")

            return

    print("Student not found!")


def statistics_report():
    print("\n--- Student Statistics Report ---")

    if not students:
        print("No student records available for statistics.")
        return

    marks_list = [student["marks"] for student in students]
    total = len(students)
    average = sum(marks_list) / total

    print("Total Students :", total)
    print(f"Average Marks  : {average:.2f}")
    print(f"Highest Marks  : {max(marks_list):.2f}")
    print(f"Lowest Marks   : {min(marks_list):.2f}")

    print("\nGrade Distribution:")
    for grade in ["A+", "A", "B", "C", "D", "F"]:
        count = sum(
            1 for student in students
            if calculate_grade(student["marks"]) == grade
        )
        print(f"Grade {grade}: {count} student(s)")


def main():
    load_students()
    print(f"Loaded {len(students)} student record(s).")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            statistics_report()
        elif choice == "7":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
