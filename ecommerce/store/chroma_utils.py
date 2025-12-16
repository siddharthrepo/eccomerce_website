import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chroma_db"))

# Global cache
_chroma_collection = None

def get_chroma_collection():
    global _chroma_collection
    if _chroma_collection is None:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        _chroma_collection = Chroma(
            collection_name="products",
            embedding_function=embedding_model,
            persist_directory=CHROMA_DB_PATH
        )
    return _chroma_collection

def add_product_to_chroma(product_id, text, embedding=None):
    chroma_collection = get_chroma_collection()
    chroma_collection.add_texts(
        [text],
        ids=[str(product_id)],
        metadatas=[{"id": str(product_id)}],
        embeddings=[embedding] if embedding is not None else None
    )

def update_product_in_chroma(product_id, text, embedding=None):
    chroma_collection = get_chroma_collection()
    delete_product_from_chroma(product_id)
    add_product_to_chroma(product_id, text, embedding)

def delete_product_from_chroma(product_id):
    chroma_collection = get_chroma_collection()
    chroma_collection.delete(ids=[str(product_id)])

def query_similar_products(text, n_results=5):
    chroma_collection = get_chroma_collection()
    results = chroma_collection.similarity_search_with_score(text, k=n_results)
    ids = []
    for doc, _ in results:
        ids.append(int(doc.metadata.get('id', 0)))
    return ids