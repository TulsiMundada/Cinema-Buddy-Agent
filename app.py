import os
import streamlit as st
from agent import generate_sql, run_query

st.title("🎬 Movie Explorer AI")

query = st.text_input("Ask something about movies:")

if query:
    # 👋 Handle greetings
    if query.lower() in ["hi", "hello", "hey"]:
        st.write("👋 Hi! I am your Movie Explorer AI 🎬")
        st.write("You can ask things like:")
        st.write("- Top rated movies")
        st.write("- Movies by Anurag Kashyap")
        st.write("- Movies starting with Z")

    else:
        sql = generate_sql(query)
        
        st.write("### Generated SQL")
        st.code(sql)

        results = run_query(sql)

        if results:
            st.write("### Results")
            for row in results:
                st.write(f"🎬 {row[0]} ({row[1]}) ⭐ {row[2]}")
        else:
            st.write("⚠️ No results found or query failed.")
