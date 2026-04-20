"""
Retriever setup and vector store configuration.
Uses FAISS (fully local, no account needed) with HuggingFace embeddings (free).
"""

import logging
import os

from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.core.config import settings

logger = logging.getLogger(__name__)

embeddings = HuggingFaceEmbeddings(model_name=settings.HUGGINGFACE_MODEL)

# Global FAISS vectorstore instance — shared between upload and retrieval
_faiss_vectorstore = None


def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in FAISS vector database.

    Args:
        chunks: List of document chunks to store.

    Returns:
        Boolean indicating success of the operation.
    """
    global _faiss_vectorstore

    try:
        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings,
        )
        _faiss_vectorstore = vectorstore
        logger.info("FAISS vector store initialized with %d document chunks", len(chunks))
        return True
    except Exception as e:
        logger.error("Error storing documents in FAISS: %s", e)
        return False


def get_retriever():
    """
    Get a retriever tool connected to the FAISS vector store.

    Returns the retriever tool that can search documents stored by retriever_chain().
    If no documents have been uploaded yet, creates a retriever with a placeholder document.

    Returns:
        A LangChain retriever tool configured for the vector store.

    Raises:
        Exception: If vector store initialization fails.
    """
    global _faiss_vectorstore

    try:
        if _faiss_vectorstore is not None:
            retriever = _faiss_vectorstore.as_retriever()
            logger.info("Using existing FAISS vectorstore with uploaded documents")
        else:
            logger.info("No documents uploaded yet, creating placeholder vectorstore")
            placeholder_doc = Document(
                page_content="No documents have been uploaded yet. Please upload a document first.",
                metadata={"source": "initialization"},
            )
            _faiss_vectorstore = FAISS.from_documents(
                documents=[placeholder_doc],
                embedding=embeddings,
            )
            retriever = _faiss_vectorstore.as_retriever()

        # Load document description if available
        description = None
        if os.path.exists("description.txt"):
            with open("description.txt", "r", encoding="utf-8") as f:
                description = f.read()

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever_customer_uploaded_documents",
            f"Use this tool **only** to answer questions about: {description}\n"
            "Don't use this tool to answer anything else.",
        )
        return retriever_tool

    except Exception as e:
        logger.error("Error initializing retriever: %s", e)
        raise Exception(e)
