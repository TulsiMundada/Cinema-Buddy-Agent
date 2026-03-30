import google.generativeai as genai
import psycopg2

# 🔑 Gemini API Key
genai.configure(api_key="xxx")


# 🤖 Model

model = genai.GenerativeModel("gemini-2.5-flash")

# 🗄️ DB connection
conn = psycopg2.connect(
    host="34.48.235.199",
    port=5432,
    database="postgres",
    user="postgres",
    password="postgres",
    sslmode="require"
)

cur = conn.cursor()

# 🎯 NL → SQL
def generate_sql(user_query):
    prompt = f"""

You are an expert PostgreSQL SQL generator.

Table: movies
Columns:
title, year, rating, runtime, genre, director, presentation

Rules:
- Use ILIKE for text search (case-insensitive, partial match)
- Always use LIMIT 5 unless user specifies otherwise
- If user asks for "top", "best", sort by rating DESC
- For names (director, genre), use partial match: ILIKE '%value%'
- Ignore NULL values when possible
- Return ONLY SQL (no markdown, no explanation)
- If no results likely, suggest top rated movies instead

Query: {user_query}
"""
    
    response = model.generate_content(prompt)
    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql

# 🔍 Execute SQL
def run_query(sql):
    try:
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        conn.rollback()   
        print("DB Error:", e)
        return []
