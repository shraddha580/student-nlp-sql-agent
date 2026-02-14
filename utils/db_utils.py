import os
import sqlite3
import pandas as pd

UPLOAD_DIR = "data"


def save_uploaded_file(uploaded_file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def execute_query(db_path: str, query: str):
    """
    Executes SQL query safely and returns structured response.
    """

    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return {
            "status": "success",
            "data": df
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

