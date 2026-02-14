# core/prompt_builder.py

def format_schema(schema: dict) -> str:
    """
    Converts schema dictionary into readable structured text for LLM.
    Expected schema format:
    {
        "table_name": [
            {"column": "col1", "type": "TYPE"},
            {"column": "col2", "type": "TYPE"}
        ]
    }
    """

    formatted_schema = "Database Schema:\n\n"

    for table_name, columns in schema.items():
        formatted_schema += f"Table: {table_name}\n"

        for col in columns:
            column_name = col.get("column")
            column_type = col.get("type")
            formatted_schema += f"  - {column_name} ({column_type})\n"

        formatted_schema += "\n"

    return formatted_schema


def build_prompt(schema: dict, user_question: str) -> str:
    """
    Builds final prompt to send to LLM.
    """

    schema_text = format_schema(schema)

    instructions = """
You are an expert SQL query generator.

Strict Rules:
1. Only generate SELECT queries.
2. Do NOT generate INSERT, UPDATE, DELETE, DROP, ALTER.
3. Use ONLY the tables and columns provided in the schema.
4. Do NOT assume any extra columns.
5. Do NOT provide explanations.
6. Return only the raw SQL query.
7. If the query cannot be generated using the schema, return: INVALID_QUERY.
"""

    final_prompt = f"""
{instructions}

{schema_text}

User Question:
{user_question}

SQL Query:
"""

    return final_prompt.strip()
