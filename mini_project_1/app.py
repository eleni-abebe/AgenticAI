from dotenv import load_dotenv
# Load all the environment variables
load_dotenv()

# Import required libraries
import streamlit as st  # to power the web UI
import os               # helps access environment variables
import sqlite3          # to interact with the database
import google.generativeai as genai  # convert natural language to SQL queries

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get SQL query from Gemini
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-2.5-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query and fetch results
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()  # A cursor lets you send SQL commands to the database
    cur.execute(sql)
    rows = cur.fetchall()  # Retrieves results as a list of tuples
    conn.close()
    for row in rows:
        print(row)
    return rows

# Define your prompt (unchanged)
prompt = [
    """
    You are an expert AI assistant specializing in converting natural language questions into SQL queries.

    The SQL database is named STUDENT and contains the following columns:

    NAME (VARCHAR)

    CLASS (VARCHAR)

    SECTION (VARCHAR)

    MARKS (INT)

    Follow these guidelines when generating SQL queries:

    Ensure the output contains only the SQL query—do not include explanations, formatting marks, or extra text.

    Use proper SQL syntax while maintaining accuracy and efficiency.

    If the query involves filtering, apply appropriate WHERE clauses.

    If an aggregation is required (e.g., counting records, averaging values), use functions like COUNT(), AVG(), etc.

    Examples:
    Question: "How many student records are present?"
    SQL Query: SELECT COUNT(*) FROM STUDENT;

    Question: "List all students in the Data Science class."
    SQL Query: SELECT * FROM STUDENT WHERE CLASS = "Data Science";
    """
]

# Streamlit UI
st.set_page_config(page_title="SQL Query Generator", page_icon="🛵")

# Display the header and logo
st.image("123.jfif", width=200)
st.markdown("Gemini App — your SQL assistant")
st.markdown("Ask any question and I will generate the SQL query for you")

# User input section
question = st.text_input('Enter your query in English', key="input")

# Submit button
submit = st.button("Generate SQL query")

if submit:
    # Get SQL query from Gemini
    response = get_gemini_response(question, prompt)
    print(response)  # corrected typo from 'resonse'

    # Execute SQL query and fetch data
    data = read_sql_query(response, "student.db")

    # Display results in Streamlit
    st.subheader("The response is")
    for row in data:
        print(row)
        st.header(str(row))
