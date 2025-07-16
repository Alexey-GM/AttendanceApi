from sqlalchemy.orm import Session
from data.models.student import Student
from data.models.student_group import StudentGroup
from data.models.attendance import Attendance

def fetch_risk_students(db: Session):
    students = db.query(Student).all()
    result = []

    for student in students:
        group_name = student.group_relation.name if student.group_relation else "—"
        
        missed_count = sum(1 for att in student.attendances if att.status == 0)

        if missed_count > 2:
            result.append({
                "full_name": f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip(),
                "group": group_name,
                "missed": missed_count
            })

    return result
