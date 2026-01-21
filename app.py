import streamlit as st 
from src.crew import run_support_crew
from dotenv import load_dotenv
import os

st.set_page_config(page_title="AI Support Agent", page_icon="🤖")

load_dotenv()

st.title("🤖 AI Customer Support Agent")
st.markdown(
    """
    Bem-vindo ao sistema de suporte automatizado.
    Este agente consulta uma vase de dados de FAQ para responder suas dúvidas sobre produtos.
    """)

with st.sidebar:
    st.header("Configurações")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY não encontrada no arquivo .env")
        st.stop()

    st.success("✅ API Key carregada")

    st.markdown("---")

    category = st.text_input("Categoria do Produto", value="Appliances")

    st.info(
        "Dica: A categoria ajuda o agente a filtrar o banco de dados de 1M de linhas "
        "antes de buscar a resposta específica."
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

user_query = st.chat_input("Digite sua pergunta sobre o produto...")


if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner(f"Pesquisando na base de dados (Categoria: {category})..."):
            try:
                result = run_support_crew(category=category, query=user_query)

                response_text = str(result)

                st.write(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")