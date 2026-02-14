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


def is_safe_query(sql: str) -> bool:
    """
    Validates that SQL query is safe and only SELECT.
    """

    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        return False

    forbidden_keywords = ["insert", "update", "delete", "drop", "alter"]

    for keyword in forbidden_keywords:
        if keyword in sql_lower:
            return False

    return True
