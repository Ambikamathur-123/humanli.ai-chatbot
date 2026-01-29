Website Question Answering Chatbot (RAG-Based)
Project Overview

This project is a Retrieval-Augmented Generation (RAG) based chatbot that answers user questions using the content of a given website.

The system first collects text from the website, stores it in a vector database, and then generates answers only from the retrieved website content. This approach helps reduce hallucinations and avoids using external knowledge.

User Interface (Streamlit)

The Streamlit app allows users to:

Enter a website URL

Index the website content

Ask questions in a chat interface

Get answers based only on the indexed website

Architecture Overview

The chatbot follows a simple and modular RAG pipeline:

User (Streamlit UI)
   ↓
Website URL
   ↓
Web Scraper
   ↓
Text Chunking (spaCy)
   ↓
Embedding Generation
   ↓
FAISS Vector Database (stored locally)
   ↓
Retriever (Top-K search)
   ↓
LLM (uses retrieved content only)
   ↓
Final Answer

Key Design Ideas

Retrieval-first approach – the model only sees website data

Strict prompts – prevents hallucinated answers

Session-based memory – keeps short chat context

Persistent embeddings – avoids reprocessing data repeatedly

Tools & Frameworks
LangChain

Used to:

Load website content

Handle chunking and retrieval

Connect embeddings, vector store, and LLM

Build the overall RAG pipeline

LangGraph was not used since this project does not need multi-agent or state-based workflows.

Language Model

Model: google/flan-t5-large

Why this model?

Open-source and free

Instruction-tuned for question answering

Good reasoning and summarization

Can run locally using Hugging Face

No paid or proprietary APIs required

The model is used only with retrieved website content.

Vector Database

FAISS

Why FAISS?

Fast similarity search

Lightweight and local

Easy to store and reload embeddings

Works well for small to medium projects

Embeddings

Model: all-MiniLM-L6-v2 (SentenceTransformers)

384-dimensional embeddings

Fast and efficient

Process:

Website text is split using spaCy

Each chunk is embedded once

Stored in FAISS

Only similarity search is done during questions

Setup & Run Instructions
1. Clone the Repository
git clone https://github.com/Ambikamathur-123/humanli.ai-chatbot.git
cd humanli.ai-chatbot

2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

4. Run the Application
streamlit run app.py

5. Open in Browser

Streamlit will show a local or public URL to access the chatbot.

Assumptions

Website has readable text content

Website allows scraping

One website per session

English language content

Limitations

JavaScript-heavy websites may not load fully

No multi-website querying

No similarity score filtering

Large websites may take longer to index

CPU-only inference can be slow

Future Improvements

Multi-page crawling with depth control

Similarity score thresholds

Support multiple websites

Show source references with answers

Add reranking with cross-encoders

GPU-based deployment

User authentication

Advanced conversation flows using LangGraph

Live Demo
https://humanliai-chatbot-9drivhypwan2ptqnxgpf2s.streamlit.app/
Final Notes

This project showcases:

End-to-end RAG implementation

Hallucination-safe question answering

Clean and modular design

Practical, production-style architectureEvaluator- and interview-friendly implementation
