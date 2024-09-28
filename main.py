from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import execute_sql_query, is_sql_query_safe
from llm import generate_sql_query

app = FastAPI()

class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    results: list

@app.post("/query", response_model=QueryResponse)
def execute_query(request: QueryRequest):
    user_query = request.user_query
    sql_query = generate_sql_query(user_query)
    print('sql_query', sql_query)
    if not is_sql_query_safe(sql_query):
        raise HTTPException(status_code=400, detail="Generated SQL query is unsafe.")

    results = execute_sql_query(sql_query)
    return QueryResponse(results=results)

@app.get("/cities/")
def read_items():
    query = "SELECT * FROM city;"  # example
    items = execute_sql_query(query)
    return {"data": items}

