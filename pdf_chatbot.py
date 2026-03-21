
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = "HumanResourcePolicy.pdf"
PERSIST_DIR = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"


def get_collection_name(pdf_path: str) -> str:
    pdf_file = Path(pdf_path)
    # Rebuild index automatically when file content timestamp changes.
    stamp = int(pdf_file.stat().st_mtime)
    safe_name = "".join(ch if ch.isalnum() else "_" for ch in pdf_file.stem.lower())
    return f"pdf_{safe_name}_{stamp}"


def build_rag_chain():
    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"PDF file not found: {PDF_PATH}. Place your PDF at this path and try again."
        )

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    if not documents:
        raise ValueError("No content found in PDF.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    collection_name = get_collection_name(PDF_PATH)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=collection_name,
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=GROQ_MODEL,
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template(
        "You are an HR assistant of icap.org.pk.Answer only from the provided HR policy document. Use only the provided context to answer. "
        "If the answer is not in the context, say you don't know.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{input}"
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain


def main():
    try:
        chain = build_rag_chain()
    except Exception as exc:
        print(f"Setup error: {exc}")
        sys.exit(1)

    print(f"PDF chatbot ready. Ask questions about {PDF_PATH}")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            response = chain.invoke({"input": user_input})
            print(f"Bot: {response['answer']}\n")
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
