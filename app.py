import streamlit as st
import pandas as pd
import sqlite3
from utils.db_utils import save_uploaded_file
from utils.schema_parser import extract_schema

st.title("Agentic Text-to-SQL System")
st.subheader("Phase 1: Database & Schema Upload")

uploaded_file = st.file_uploader(
    "Upload a student database (CSV or SQLite .db)",
    type=["csv", "db"]
)

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(file_path)
        db_path = "data/temp.db"
        conn = sqlite3.connect(db_path)
        df.to_sql("students", conn, if_exists="replace", index=False)
        conn.close()
    else:
        db_path = file_path

    schema = extract_schema(db_path)

    st.success("Schema extracted successfully!")
    st.json(schema)

