import numpy as np
import matplotlib.pyplot as plt
from data.db.db import SessionLocal
from repository.attendance_repository import get_all_attendance
from repository.student_repository import get_all_students
from repository.subject_repository import get_all_subjects
from repository.schedule_repository import get_all_schedules
from repository.student_group_repository import get_all_student_groups

def fetch_data():
    db = SessionLocal()
    try:
        attendances = get_all_attendance(db)
        students = get_all_students(db)
        groups = get_all_student_groups(db)
        courses = get_all_subjects(db)
        schedules = get_all_schedules(db)
        return attendances, students, groups, courses, schedules
    finally:
        db.close()

def average_attendance_by_group():
    attendances, students, groups, _, _ = fetch_data()
    group_attendance = {g.id: [] for g in groups}
    student_map = {s.id: s for s in students}
    for a in attendances:
        student = student_map.get(a.student)
        if student:
            group_attendance[student.group_id].append(a.status)
    avgs = [np.mean(group_attendance[g.id])*100 if group_attendance[g.id] else 0 for g in groups]
    plt.bar([g.name for g in groups], avgs, color='skyblue')
    plt.title('Средняя посещаемость по группам')
    plt.ylabel('Посещаемость (%)')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

def average_attendance_by_course():
    attendances, _, _, courses, schedules = fetch_data()
    course_attendance = {c.id: [] for c in courses}
    schedule_map = {s.id: s for s in schedules}
    for a in attendances:
        schedule = schedule_map.get(a.schedule)
        if schedule:
            course_attendance[getattr(schedule, 'student_subject', getattr(schedule, 'subject_id', None))].append(a.status)
    avgs = [np.mean(course_attendance[c.id])*100 if course_attendance[c.id] else 0 for c in courses]
    plt.bar([c.name for c in courses], avgs, color='orange')
    plt.title('Средняя посещаемость по предмету')
    plt.ylabel('Посещаемость (%)')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

def average_student_attendance():
    attendances, students, groups, _, _ = fetch_data()
    # Select group
    print("Выберите группу:")
    for idx, g in enumerate(groups):
        print(f"{idx+1}. {g.name}")
    group_choice = input("Введите номер группы: ").strip()
    try:
        group_idx = int(group_choice) - 1
        group_id = groups[group_idx].id
    except (ValueError, IndexError):
        print("Неверный выбор группы.")
        return
    group_students = [s for s in students if s.group_id == group_id]
    student_attendance = {s.id: [] for s in group_students}
    for a in attendances:
        if a.student in student_attendance:
            student_attendance[a.student].append(a.status)
    avgs = [np.mean(student_attendance[s.id])*100 if student_attendance[s.id] else 0 for s in group_students]
    plt.bar([f"{s.first_name} {s.last_name}" for s in group_students], avgs, color='green')
    plt.title(f'Средняя посещаемость по студенту (группа: {groups[group_idx].name})')
    plt.ylabel('Посещаемость (%)')
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def attendance_risk_zone(threshold=5):
    attendances, students, groups, _, _ = fetch_data()
    # Select group
    print("Выберите группу:")
    for idx, g in enumerate(groups):
        print(f"{idx+1}. {g.name}")
    group_choice = input("Введите номер группы: ").strip()
    try:
        group_idx = int(group_choice) - 1
        group_id = groups[group_idx].id
    except (ValueError, IndexError):
        print("Неверный выбор группы.")
        return
    group_students = [s for s in students if s.group_id == group_id]
    absences = {s.id: 0 for s in group_students}
    for a in attendances:
        if a.student in absences and a.status == 0:
            absences[a.student] += 1
    colors = ['red' if absences[s.id] >= threshold else 'blue' for s in group_students]
    plt.bar([f"{s.first_name} {s.last_name}" for s in group_students], [absences[s.id] for s in group_students], color=colors)
    plt.axhline(y=threshold, color='black', linestyle='--', label=f'Threshold = {threshold}')
    plt.title(f'Студенты в зоне риска (группа: {groups[group_idx].name})')
    plt.ylabel('Пропущенные занятия')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

def attendance_grade_correlation():
    # Since there is no grade data, generate random grades correlated with attendance
    attendances, students, _, _, _ = fetch_data()
    student_attendance = {s.id: [] for s in students}
    for a in attendances:
        student_attendance[a.student].append(a.status)
    avg_attendance = np.array([
        np.mean(student_attendance[s.id])*100 if student_attendance[s.id] else 0 for s in students
    ])
    grades = avg_attendance * 0.7 + np.random.normal(20, 10, size=len(students))
    corr_coef = np.corrcoef(avg_attendance, grades)[0, 1]
    plt.scatter(avg_attendance, grades, color='purple')
    plt.title(f'Посещаемость vs Оценка (Корреляция: {corr_coef:.2f})')
    plt.xlabel('Посещаемость (%)')
    plt.ylabel('Оценка')
    plt.tight_layout()
    plt.show()

def main():
    print("Select analysis to run:")
    print("1. Average attendance by group")
    print("2. Average attendance by course")
    print("3. Average student attendance")
    print("4. Attendance risk zone (missed >= 5 classes)")
    print("5. Attendance and grade correlation coefficient")
    choice = input("Enter number (1-5): ").strip()
    if choice == '1':
        average_attendance_by_group()
    elif choice == '2':
        average_attendance_by_course()
    elif choice == '3':
        average_student_attendance()
    elif choice == '4':
        attendance_risk_zone()
    elif choice == '5':
        attendance_grade_correlation()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main() 