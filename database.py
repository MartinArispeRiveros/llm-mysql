import json
import mysql.connector
from mysql.connector import Error
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

from settings import db_url, db_user, db_pass, db_name

db_config = {
    "host": db_url,
    "user": db_user,
    "password": db_pass,
    "database": db_name
}


def execute_sql_query(query: str) -> List[Dict]:
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Error as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_database_schema() -> str:
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Retrieve All Tables
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s", (db_config['database'],))
        tables = cursor.fetchall()

        # Initialize the schema dictionary
        database_schema = {}

        # Retrieve Schema Information for Each Table
        for table in tables:
            table_name = table['TABLE_NAME']

            # Get column details for each table
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s
            """, (table_name, db_config['database']))
            columns = cursor.fetchall()

            # Get primary key information
            cursor.execute(f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_NAME = %s AND CONSTRAINT_NAME = 'PRIMARY' AND TABLE_SCHEMA = %s
            """, (table_name, db_config['database']))
            primary_keys = cursor.fetchall()

            # Organize the table schema
            database_schema[table_name] = {
                "columns": columns,
                "primary_keys": [key["COLUMN_NAME"] for key in primary_keys]
            }

        # Convert the Schema to JSON
        database_schema_json = json.dumps(database_schema, indent=4)
        return database_schema_json

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def is_sql_query_safe(sql_query):
    prohibited_phrases = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
        "EXEC", "--", ";", "/*", "*/", "@@", "@", "CREATE", "SHUTDOWN",
        "GRANT", "REVOKE"
    ]
    for phrase in prohibited_phrases:
        if phrase.lower() in sql_query.lower():
            return False
    return True
