import re

ALLOWED_TABLES = {"students", "courses", "enrollments"}

def validate_sql(sql: str):
    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    forbidden = ["delete", "drop", "update", "insert", "alter"]
    if any(word in sql_lower for word in forbidden):
        raise ValueError("Forbidden SQL operation detected")

    tables = re.findall(r'from\s+(\w+)|join\s+(\w+)', sql_lower)
    used_tables = {t for pair in tables for t in pair if t}

    if not used_tables.issubset(ALLOWED_TABLES):
        raise ValueError("Unauthorized table used")

    return True