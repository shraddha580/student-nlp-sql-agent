# core/sql_validator.py

import re


def clean_sql_output(sql: str) -> str:
    """
    Cleans markdown formatting or extra text from LLM output.
    """

    # Remove markdown backticks if present
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    return sql.strip()


def is_safe_query(query: str):
    query_clean = query.strip()
    query_lower = query_clean.lower()

    # Block LLM failure outputs
    if query_clean == "" or query_lower == "invalid_query":
        return False, "The system could not generate a valid SQL query."

    # Must start with SELECT
    if not query_lower.startswith("select"):
        return False, "Only SELECT statements are allowed."

    # Block dangerous keywords
    forbidden = ["drop", "delete", "update", "insert", "alter"]

    for word in forbidden:
        if word in query_lower:
            return False, "Only SELECT statements are allowed."

    return True, "Query is safe."


