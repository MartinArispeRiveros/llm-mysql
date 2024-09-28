import openai
from dotenv import load_dotenv
from settings import openai_api_key
from database import get_database_schema

load_dotenv()


def generate_sql_query(user_query):
    database_schema = get_database_schema()
    print('database_schema', database_schema)
    system_message = f"""
     Given the following schema, wrute a SQL query that retrieves the requested information.
     Return the SQL qeury inside a JSON structure with the key "sql_query".
     <example>{{
         "sql_query": "SELECT * fROM users WHERE age > 18;"
         "original_query": "Show me all users older than 18 years old"
     }}
     </example>
     <schema>
        {database_schema}
     </schema>
     """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ]   
    )
    return response.choices[0].message.content
