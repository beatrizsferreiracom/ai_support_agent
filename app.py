import streamlit as st
from src.crew import run_support_crew
from src.db import get_categories, get_products_by_category
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI Support Agent",
    page_icon="🤖",
    layout="centered"
)

load_dotenv()

st.title("🤖 AI Customer Support Agent")
st.markdown(
    """
    This assistant answers product questions using an internal FAQ database.
    Select a **category** and a **product** before asking your question.
    """
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("Settings")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY not found in .env")
        st.stop()

    st.success("✅ API Key loaded")
    st.markdown("---")

    categories = get_categories()
    category = st.selectbox(
        "Product Category",
        categories
    )

    products = get_products_by_category(category)
    product = st.selectbox(
        "Product",
        products,
        help="Select the product you want to ask about"
    )

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_product" not in st.session_state:
    st.session_state.selected_product = product

# Update selected product
st.session_state.selected_product = product

# --------------------------------------------------
# Product Context Display
# --------------------------------------------------

st.markdown(
    f"""
    ### 🧾 Selected Product
    **{st.session_state.selected_product}**
    """
)

st.divider()

# --------------------------------------------------
# Initial Assistant Message
# --------------------------------------------------

if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Hello! 👋\n\n"
            "You can ask questions about the selected product.\n"
            "For example: *weight*, *color*, *dimensions*, *compatibility*."
        )
    })

# --------------------------------------------------
# Render Chat
# --------------------------------------------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --------------------------------------------------
# Input
# --------------------------------------------------

user_query = st.chat_input("Ask something about the product...")

# --------------------------------------------------
# Main Flow
# --------------------------------------------------

if user_query:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })
    st.chat_message("user").write(user_query)

    # Inject product context (light memory)
    contextual_query = (
        f"Considering the product {st.session_state.selected_product}, "
        f"{user_query}"
    )

    with st.chat_message("assistant"):
        with st.spinner("Searching the FAQ database..."):
            result = run_support_crew(
                category=category,
                product=st.session_state.selected_product,
                query=contextual_query
            )

            response_text = str(result)[:2000]

            st.write(response_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })