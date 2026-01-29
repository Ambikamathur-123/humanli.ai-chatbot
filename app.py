import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from chain import ask_question
from vector_embeddings import create_vector_store, load_vector_store
from web_scraping import scrape_url, ScraperError
from pdf_loader import semantic_chunking
from save_scrape_data import save_text_to_pdf

# =============================
# PAGE CONFIG (UI ONLY)
# =============================
st.set_page_config(
    page_title="Humanli.AI – Website Assistant",
    page_icon="🤖",
    layout="wide"
)

# =============================
# CUSTOM UI STYLING (SAFE)
# =============================
st.markdown("""
<style>
.main {
    background-color: #f6f8ff;
}
h1, h2, h3 {
    color: #2c2c54;
}
.stButton>button {
    background-color: #5f27cd;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
}
.stTextInput>div>div>input {
    border-radius: 8px;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR (UI ONLY)
# =============================
with st.sidebar:
    st.title("🤖 Humanli.AI")
    st.markdown("**Website Question Answering System**")
    st.markdown("---")
    st.markdown("🔹 Enter a website URL")
    st.markdown("🔹 Index website content")
    st.markdown("🔹 Ask AI-powered questions")
    st.markdown("---")
    st.caption("Assignment UI Version")

# =============================
# MAIN HEADER
# =============================
st.title("🌐 Humanli.AI – Website QA Chatbot")
st.caption("Ask intelligent questions from any website using AI")
st.markdown("---")

# =============================
# SESSION STATE (UNCHANGED)
# =============================
if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat" not in st.session_state:
    st.session_state.chat = []

# =============================
# URL INPUT SECTION
# =============================
st.subheader("🔗 Step 1: Enter Website URL")

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

# =============================
# INDEX WEBSITE (LOGIC SAME)
# =============================
if st.button("📥 Index Website"):
    if not url:
        st.error("Please enter a valid website URL.")
    else:
        with st.spinner("Scraping and indexing website..."):
            try:
                content = scrape_url(url)
                save_text_to_pdf(
                    text=content,
                    filename="web_scraping_article.pdf"
                )
            except ScraperError as e:
                st.error(f"Error while scraping: {e}")

            loader = PyPDFLoader("web_scraping_article.pdf")
            docs = loader.load()
            semantic_chunks = semantic_chunking(docs, max_chars=500)

            create_vector_store(semantic_chunks)

            st.session_state.indexed = True
            st.success("✅ Website indexed successfully!")

# =============================
# CHAT SECTION
# =============================
st.subheader("💬 Step 2: Ask Questions")

if not st.session_state.indexed:
    st.info("Please index a website first to start chatting.")
else:
    user_question = st.chat_input("Type your question here...")

    if user_question:
        answer = ask_question(user_question)
        st.session_state.chat.append(
            {"question": user_question, "answer": answer}
        )

    for msg in st.session_state.chat:
        with st.chat_message("user"):
            st.write(msg["question"])
        with st.chat_message("assistant"):
            st.write(msg["answer"])

# =============================
# FOOTER
# =============================
st.markdown("---")
st.markdown(
    "<center>Made by <b>Ambika Mathur</b> | AI Assignment Project</center>",
    unsafe_allow_html=True
)
