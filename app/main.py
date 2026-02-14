from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlalchemy
import time
import re
from collections import Counter

from app.database import engine
from app.models import Base
from app.llm import question_to_sql
from app.validator import validate_sql
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed database
    seed_data()

    yield


app = FastAPI(lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str


query_logs = []


@app.post("/query")
def run_query(request: QueryRequest):
    try:
        start = time.time()

        sql = question_to_sql(request.question)

        validate_sql(sql)

        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(sql))
            rows = result.fetchall()

        # Clean result formatting
        if len(rows) == 1 and len(rows[0]) == 1:
            data = rows[0][0]
        else:
            data = [list(row) for row in rows]

        execution_time = time.time() - start

        query_logs.append({
            "question": request.question,
            "execution_time": execution_time,
            "sql": sql
        })

        return {
            "generated_sql": sql,
            "result": data,
            "execution_time": execution_time
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats")
def stats():
    if not query_logs:
        return {
            "total_queries": 0,
            "average_execution_time": 0,
            "slowest_query": None,
            "most_common_keywords": []
        }

    total_queries = len(query_logs)
    avg_time = sum(q["execution_time"] for q in query_logs) / total_queries
    slowest = max(query_logs, key=lambda x: x["execution_time"])

    words = []
    for q in query_logs:
        tokens = re.findall(r'\b\w+\b', q["question"].lower())
        words.extend(tokens)

    stopwords = {"how", "many", "in", "the", "is", "are", "of", "a"}
    filtered_words = [w for w in words if w not in stopwords]
    most_common = Counter(filtered_words).most_common(5)

    return {
        "total_queries": total_queries,
        "average_execution_time": round(avg_time, 4),
        "slowest_query": slowest,
        "most_common_keywords": most_common
    }