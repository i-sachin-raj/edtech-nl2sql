import os
from google import genai
from dotenv import load_dotenv
import google
# Load environment variables
load_dotenv()
# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# System prompt with schema context
SYSTEM_PROMPT = """
You are an expert SQLite SQL generator.

Database Schema (all table names are lowercase):

students(id, name, grade, created_at)
courses(id, name, category)
enrollments(id, student_id, course_id, enrolled_at)

Relationships:
- enrollments.student_id → students.id
- enrollments.course_id → courses.id

Rules:
- Only generate SELECT queries.
- Use SQLite syntax.
- ALL table names MUST be lowercase exactly as shown.
- ALL column names MUST match schema exactly.
- All string comparisons must be case-insensitive.
- Use COLLATE NOCASE for string matching.
- Do NOT explain anything.
- Do NOT use markdown.
- Return ONLY raw SQL.
"""
def question_to_sql(question: str) -> str:
    """
    Converts natural language question to SQLite SQL using Google Gemini.
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=SYSTEM_PROMPT + "\n\nUser Question: " + question
        )

        sql = response.text.strip()

        # Remove accidental markdown if model adds it
        if sql.startswith("```"):
            sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql

    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")