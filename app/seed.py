from .database import engine, SessionLocal
from .models import Base, Student, Course, Enrollment
from datetime import datetime
import random


def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Prevent duplicate seeding
    if db.query(Student).first():
        db.close()
        return

    # ------------------------
    # Students (10)
    # ------------------------
    students = [
        Student(name=f"student{i}", grade="A")
        for i in range(1, 11)
    ]
    db.add_all(students)

    # ------------------------
    # Courses (lowercase names)
    # ------------------------
    courses = [
        Course(name="python", category="programming"),
        Course(name="java", category="programming"),
        Course(name="math", category="stem"),
        Course(name="physics", category="stem"),
        Course(name="ai", category="tech"),
    ]
    db.add_all(courses)

    db.commit()

    # ------------------------
    # Enrollments (20+ with year variation)
    # ------------------------
    for _ in range(25):
        enrollment = Enrollment(
            student_id=random.randint(1, 10),
            course_id=random.randint(1, 5),
            enrolled_at=datetime(
                random.choice([2023, 2024, 2025]),  # year variation
                random.randint(1, 12),
                random.randint(1, 28),
            ),
        )
        db.add(enrollment)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_data()