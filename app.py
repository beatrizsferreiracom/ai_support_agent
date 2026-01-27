import streamlit as st 
from src.crew import run_support_crew
from dotenv import load_dotenv
import os

st.set_page_config(page_title="AI Support Agent", page_icon="🤖")

load_dotenv()

st.title("🤖 AI Customer Support Agent")
st.markdown(
    """
    Welcome to the automated support system.
    This agent consults a FAQ database to answer your product questions.
    """)

with st.sidebar:
    st.header("Settings")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY not found in the file .env")
        st.stop()

    st.success("✅ API Key loaded")

    st.markdown("---")

    category = st.text_input("Product Category", value="Appliances")

    st.info(
        "Tip: The category helps the agent filter the database "
        "before searching for the specific answer."
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você hoje?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

user_query = st.chat_input("Type your question about the product...")

if user_query and user_query.isdigit() and st.session_state.pending_options:
    idx = int(user_query) - 1

    if 0 <= idx < len(st.session_state.pending_options):
        user_query = st.session_state.pending_options[idx]
        st.session_state.pending_options = None
    else:
        st.error("Opção inválida.")
        st.stop()

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner(f"Searching the database (Category: {category})..."):
            try:
                result = run_support_crew(category=category, query=user_query)

                response_text = str(result)[:2000]

                lines = response_text.splitlines()
                options = []

                for line in lines:
                    if line.strip().startswith(tuple("123456789")):
                        option = line.split(".", 1)[1].strip()
                        options.append(option)

                if options:
                    st.session_state.pending_options = options

                st.write(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"An error occurred: {e}")