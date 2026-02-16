
#  Agentic Text-to-SQL System

A schema-adaptive, secure Text-to-SQL system that converts natural language questions into safe, executable SQL queries on user-uploaded databases.

The system dynamically understands the uploaded database structure and generates read-only SQL queries using an LLM, ensuring safe and reliable execution.

---

##  Architecture Overview

```
User Question (Natural Language)
        ↓
Database Schema Extraction
        ↓
Prompt Builder (Schema + Question)
        ↓
LLM SQL Generation
        ↓
SQL Cleaning
        ↓
Safety Validation Layer
        ↓
Execution Engine (SQLite)
        ↓
Error Classification & Retry (if needed)
        ↓
Final Result Display
```

---

##  Workflow

1. User uploads a CSV or SQLite database.
2. The system automatically extracts tables and columns.
3. The user enters a natural language question.
4. A schema-aware prompt is constructed and sent to the LLM.
5. The generated SQL is cleaned and validated.
6. The Safety Layer enforces:

   * SELECT-only execution
   * Blocking of destructive operations
   * Prevention of multi-statement queries
7. The query is executed securely.
8. If execution fails, the system classifies the error and attempts automatic correction.
9. The final result (or structured error message) is displayed.

---

##  Design Principles

* Schema-aware generation
* Read-only secure execution
* Guardrail-based validation
* Structured error handling
* Agentic retry mechanism




