import sqlite3

def extract_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema = {}

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        schema[table_name] = [
            {"column": col[1], "type": col[2]}
            for col in columns
        ]

    conn.close()
    return schema
