import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')))

from llm_interface import handle_query
from graph_builder import build_graph
from graph_ui import generate_graph_html

# 🔥 Build graph once
build_graph()

st.set_page_config(layout="wide")

st.title("📊 Graph-Based Business Query System")

# ✅ Split screen
col1, col2 = st.columns([2, 1])

# -------------------------------
# 🧠 LEFT SIDE → GRAPH
# -------------------------------
with col1:
    st.subheader("🔗 Graph Visualization")

    html_file = generate_graph_html()

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=600, scrolling=True)

# -------------------------------
# 💬 RIGHT SIDE → CHAT
# -------------------------------
with col2:
    st.subheader("💬 Query Interface")

    user_input = st.text_input("Ask your question:")

    if st.button("Submit"):
        if user_input:
            response = handle_query(user_input)
            st.markdown("### 📌 Answer")
            st.write(response)