from core.llm_client import generate_sql_from_llm
from core.sql_validator import clean_sql_output


def correct_sql(original_sql: str, error_message: str, schema: str) -> str:
    """
    Sends failed SQL + error back to LLM for correction.
    """

    correction_prompt = f"""
The following SQL query failed during execution.

Original SQL:
{original_sql}

Database Error:
{error_message}

Database Schema:
{schema}

Fix the SQL query.
Return ONLY a valid SELECT SQL query.
Do not include explanations.
Do not include comments.
"""

    response = generate_sql_from_llm(correction_prompt)

    return clean_sql_output(response)
