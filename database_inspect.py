from app.database import engine
from app.models import Base  # IMPORTANT: import Base from models
from app.seed import seed_data
from sqlalchemy import text

def inspect_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed data safely
    seed_data()

    with engine.connect() as conn:

        print("\n===== STUDENTS =====")
        students = conn.execute(text("SELECT * FROM students")).fetchall()
        for row in students:
            print(dict(row._mapping))

        print("\n===== COURSES =====")
        courses = conn.execute(text("SELECT * FROM courses")).fetchall()
        for row in courses:
            print(dict(row._mapping))

        print("\n===== ENROLLMENTS =====")
        enrollments = conn.execute(text("SELECT * FROM enrollments")).fetchall()
        for row in enrollments:
            print(dict(row._mapping))


if __name__ == "__main__":
    inspect_database()