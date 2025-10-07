from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Import required libraries
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

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
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# Prompt (unchanged)
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
st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🛵",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .header-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        border-radius: 50%;
    }
    .main-title {
        text-align: center;
        color: #4B8BBE;
        font-size: 36px;
        font-weight: bold;
        margin-top: 10px;
    }
    .subtitle {
        text-align: center;
        color: #306998;
        font-size: 20px;
        margin-bottom: 40px;
    }
    .stButton>button {
        background-color: #FFD43B;
        color: #000;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        width: 200px;
        font-size: 18px;
    }
    .stTextInput>div>div>input {
        height: 40px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.image("123.jfif", width=150, output_format="JPEG")
st.markdown('<div class="main-title">Gemini App</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your SQL assistant — ask any question and I will generate the SQL query for you</div>', unsafe_allow_html=True)

# Input and button in a centered container
with st.container():
    question = st.text_input('Enter your query in English', key="input")
    submit = st.button("Generate SQL query")

# Display results in a neat table
if submit and question.strip() != "":
    with st.spinner("Generating SQL query..."):
        response = get_gemini_response(question, prompt)
    
    st.success("✅ SQL Query Generated!")
    st.code(response, language="sql")
    
    # Execute query and show data
    data = read_sql_query(response, "student.db")
    if data:
        st.subheader("Query Results")
        st.table(data)
    else:
        st.warning("No results found for this query.")
