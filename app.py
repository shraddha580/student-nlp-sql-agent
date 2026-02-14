import streamlit as st
import pandas as pd
import sqlite3

from utils.db_utils import save_uploaded_file, execute_query
from utils.schema_parser import extract_schema

from core.prompt_builder import build_prompt
from core.llm_client import generate_sql_from_llm
from core.sql_validator import clean_sql_output, is_safe_query
from core.correction_agent import correct_sql


MAX_RETRIES = 2


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
                query = clean_sql_output(raw_sql)

                # -------------------------------
                # Safety Validation (ONLY block dangerous queries)
                # -------------------------------

                is_valid, message = is_safe_query(query)

                if not is_valid:
                    st.error(message)
                else:

                    st.success("SQL Generated:")
                    st.code(query, language="sql")

                    # -------------------------------
                    # Silent Retry Execution Loop
                    # -------------------------------

                    retries = 0
                    final_result = None
                    last_error = None

                    while retries <= MAX_RETRIES:

                        result = execute_query(db_path, query)

                        if result["status"] == "success":
                            final_result = result
                            break
                        else:
                            last_error = result["error"]

                            query = correct_sql(
                                original_sql=query,
                                error_message=last_error,
                                schema=schema
                            )

                            # Safety check again after correction
                            is_valid, message = is_safe_query(query)

                            if not is_valid:
                                last_error = message
                                break

                            retries += 1

                    # -------------------------------
                    # Final Response to User
                    # -------------------------------

                    if final_result:
                        st.success("Query executed successfully!")
                        st.dataframe(final_result["data"])
                    else:
                        if last_error:
                            error_message = last_error.lower()

                            if "no such column" in error_message:
                                st.error("The requested column does not exist in the database.")
                            elif "no such table" in error_message:
                                st.error("The requested table does not exist in the database.")
                            elif "only select" in error_message:
                                st.error("Only SELECT statements are allowed.")
                            else:
                                st.error("There was an issue executing your request. Please rephrase your question.")
                        else:
                            st.error("Sorry, I couldn't process your question. Please rephrase it.")

            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")
