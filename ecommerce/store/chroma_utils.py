from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# Set ChromaDB persist directory (relative to this file)
CHROMA_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chroma_db"))

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

chroma_collection = Chroma(
    collection_name="products",
    embedding_function=embedding_model,
    persist_directory=CHROMA_DB_PATH
)

def add_product_to_chroma(product_id, text, embedding=None):
    chroma_collection.add_texts(
        [text],
        ids=[str(product_id)],
        metadatas=[{"id": str(product_id)}],
        embeddings=[embedding] if embedding is not None else None
    )

def update_product_in_chroma(product_id, text, embedding=None):
    delete_product_from_chroma(product_id)
    add_product_to_chroma(product_id, text, embedding)

def delete_product_from_chroma(product_id):
    chroma_collection.delete(ids=[str(product_id)])

def query_similar_products(text, n_results=9):
    results = chroma_collection.similarity_search_with_score(text, k=n_results)
    ids = []
    for doc, _ in results:
        ids.append(int(doc.metadata.get('id', 0)))
    return ids
