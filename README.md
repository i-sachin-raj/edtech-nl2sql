# EdTech NL2SQL Backend Service

An AI-powered backend service that converts natural language questions into SQL queries and returns results from an EdTech database.  
The system is designed for non-technical users to query structured data safely using natural language.

---

## Objective
Build a backend service where users can ask questions like:

> *“How many students enrolled in Python courses in 2024?”*

and receive:
- The generated SQL query
- The query result
- The execution time

---

## Tech Stack

- **FastAPI** – Backend framework
- **SQLite** – Database
- **Google Gemini (LLM)** – NLP to SQL conversion
- **SQLAlchemy** – Database execution
- **pytest** – Unit testing
- **Docker** – Containerization
- **Kubernetes** – Deployment configuration

---
## **Project Structure**

```
edtech-nl2sql/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   ├── models.py
│   ├── database.py
│   ├── validator.py
│   └── seed.py
│
├── tests/
│   ├── test_api.py
│   └── test_validator.py
│
├── Dockerfile
├── k8s.yaml
├── requirements.txt
├── README.md
└── .gitignore
```
---
## **Running Locally**

### **Create Virtual Environment**
```
python -m venv venv
source venv/bin/activate
```

### **Install Dependencies**
```
pip install -r requirements.txt
```

### **Run the Server**
```
uvicorn app.main:app --reload
```

Open:
```
http://127.0.0.1:8000/docs
```

---
## **Running Tests**
Unit tests cover:
- API endpoints
- SQL validator logic
Run tests using:
```
pytest
```

---
## **Docker**
### **Build Image**
```
docker build -t edtech-nl2sql .
```

### **Run Container**
```
docker run -p 8000:8000 --env-file .env edtech-nl2sql
```

---

### **Generating a Google Gemini API Key**

  

Follow these steps:

1. Go to: https://aistudio.google.com/
2. Sign in with your Google account.
3. Click **“Get API Key”** (top right).
4. Click **Create API Key**.
5. Copy the generated key.

---

### **Setting Up the API Key**

  

Create a .env file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```


  

The application loads the API key automatically using python-dotenv.


---
## Database Schema

### Tables

```text
students(id, name, grade, created_at)
courses(id, name, category)
enrollments(id, student_id, course_id, enrolled_at)
````

### **Relationships**
- enrollments.student_id → students.id
- enrollments.course_id → courses.id

---
## **LLM Configuration**
This project uses **Google Gemini API** for natural language to SQL conversion.

### **Default Model**
By default, the system uses:
```
models/gemini-2.5-flash-lite
```

This model provides
- Fast inference
- Low latency
- Cost efficiency
- Good structured reasoning for SQL generation
---

### **Changing the Model**
To change the model, open:
```
app/llm.py
```
Find this line:
```
model="models/gemini-2.5-flash-lite"
```
Replace it with any supported model, for example:
```
model="models/gemini-2.5-flash"
```
or
```
model="models/gemini-2.0-flash-001"
```
Available models can be listed using:
```
for model in client.models.list():
    print(model.name)
```
Refer to Google AI documentation for updated model names.

---

### **Important Notes**

- If you receive a 429 RESOURCE_EXHAUSTED error, you may need to enable billing in Google Cloud.
    
- Only SELECT queries are allowed for safety.
    
- String matching is case-insensitive using COLLATE NOCASE.
    
---
## **API Endpoints**
### **POST**  **/query**
Converts a natural language question into SQL and executes it safely.
**Request Body**
```
{
  "question": "How many students enrolled in Python courses in 2024?"
}
```

**Response**
```
{
  "generated_sql": "SELECT COUNT(DISTINCT ...)",
  "result": 1,
  "execution_time": 2.58
}
```

---
### **GET**  **/stats**
Returns analytics about query usage.
**Response**
```
{
  "total_queries": 3,
  "average_execution_time": 2.13,
  "slowest_query": {
    "question": "...",
    "execution_time": 2.58
  },
  "most_common_keywords": [
    ["python", 3],
    ["students", 2]
  ]
}
```

---
## **NLP to SQL (LLM-based Approach)**
- Uses **Google Gemini** to convert natural language into SQL.
- Prompt is schema-aware to reduce hallucinations.
- Only **SELECT** queries are allowed.
- Any dangerous SQL (DELETE, DROP, UPDATE, etc.) is blocked.

This ensures:
- Security
- Read-only database access
- Safe execution

---
## **SQL Safety Validation**
Before execution:
- SQL is validated to ensure it starts with SELECT
- Blacklisted keywords are rejected
- Invalid or unsafe queries raise an error

---
## **Kubernetes**
A Kubernetes Pod configuration is provided in k8s.yaml with resource limits:

```
resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
```

This satisfies deployment and resource constraint requirements.

---
## **Summary**
This project demonstrates:
- LLM-based NLP to SQL conversion
- Secure SQL execution
- Clean API design
- Analytics and observability
- Testing, Dockerization, and Kubernetes readiness

The system is production-inspired and safe for non-technical users.

---
**Author** 
Sachin