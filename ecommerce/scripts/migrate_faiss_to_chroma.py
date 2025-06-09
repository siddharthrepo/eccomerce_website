import sys
import os
import pandas as pd
import faiss
import numpy as np

# Add the parent directory of 'store' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from store.chroma_utils import add_product_to_chroma

# Paths (adjust if needed)
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backup/description.csv'))
INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../recommendation_system/index'))

def create_textual_representation(row):
    return f"""
        id:{row['id']},
        ProductName:{row['name']},
        Brand: {row.get('Brand', '')},
        Category:{row.get('catgory', '')},
        SubCategory:{row.get('sub_catgory', '')},
        Description: {row.get('description', '')}
    """

def main():
    df = pd.read_csv(CSV_PATH)
    index = faiss.read_index(INDEX_PATH)
    n = min(index.ntotal, len(df))
    if index.ntotal != len(df):
        print(f"Warning: FAISS index ({index.ntotal}) and CSV ({len(df)}) row count mismatch! Migrating {n} entries.")

    for i, row in df.iloc[:n].iterrows():
        product_id = row['id']
        text = create_textual_representation(row)
        embedding = np.zeros((index.d,), dtype='float32')
        index.reconstruct(i, embedding)
        add_product_to_chroma(product_id, text, embedding.tolist())
        if i % 100 == 0:
            print(f"Migrated {i+1} products...")
    print("Migration to ChromaDB complete.")

if __name__ == "__main__":
    main()
