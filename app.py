import streamlit as st
import pandas as pd
import sqlite3

from utils.db_utils import save_uploaded_file
from utils.schema_parser import extract_schema

from core.prompt_builder import build_prompt
from core.llm_client import generate_sql_from_llm
from core.sql_validator import clean_sql_output, is_safe_query


st.set_page_config(page_title="Agentic Text-to-SQL", layout="wide")

st.title("Agentic Text-to-SQL System")
st.subheader("Upload Database & Ask Questions")


# -------------------------------
# File Upload Section
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload a student database (CSV or SQLite .db)",
    type=["csv", "db"]
)

if uploaded_file:

    file_path = save_uploaded_file(uploaded_file)

    # If CSV → convert to SQLite
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(file_path)
        db_path = "data/temp.db"
        conn = sqlite3.connect(db_path)
        df.to_sql("students", conn, if_exists="replace", index=False)
        conn.close()
    else:
        db_path = file_path

    # Extract schema
    schema = extract_schema(db_path)

    st.success("Schema extracted successfully!")
    st.json(schema)

    st.divider()

    # -------------------------------
    # NLP Question Section
    # -------------------------------

    st.subheader("Ask a Question")

    user_question = st.text_input(
        "Enter your question in natural language:"
    )

    if st.button("Generate SQL"):

        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                # Build prompt
                prompt = build_prompt(schema, user_question)

                # Call LLM
                raw_sql = generate_sql_from_llm(prompt)

                # Clean output
                clean_sql = clean_sql_output(raw_sql)

                # Validate SQL
                if is_safe_query(clean_sql):
                    st.success("SQL generated successfully!")
                    st.code(clean_sql, language="sql")
                else:
                    st.error("Generated SQL is unsafe or invalid.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
