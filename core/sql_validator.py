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


def is_safe_query(sql: str) -> tuple[bool, str]:
    """
    Validates that SQL query is safe and only SELECT.
    Returns (is_valid, message)
    """

    if not sql:
        return False, "Query is empty."

    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    # 1️⃣ Must start with SELECT
    if not sql_lower.startswith("select"):
        return False, "Only SELECT statements are allowed."

    # 2️⃣ Block multi-statements
    if ";" in sql_clean[:-1]:  # allow optional semicolon only at end
        return False, "Multiple SQL statements are not allowed."

    # 3️⃣ Block SQL comments
    if "--" in sql_lower or "/*" in sql_lower or "*/" in sql_lower:
        return False, "SQL comments are not allowed."

    # 4️⃣ Block forbidden keywords (whole word match)
    forbidden_keywords = [
        "insert", "update", "delete", "drop",
        "alter", "truncate", "create", "exec"
    ]

    for keyword in forbidden_keywords:
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, sql_lower):
            return False, f"Forbidden keyword detected: {keyword.upper()}"

    return True, "Query is safe."
