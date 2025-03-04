import pandas as pd
import numpy as np 
import google.generativeai as genai
import faiss


def recommend(df , id , index):
    temp = df[df['id'] == id]
    rec = temp['textual_representation'].iloc[0]
    res = genai.embed_content(
            model="models/text-embedding-004",
            # content= sample_product
            content = rec
        )
    embedding = np.array([res["embedding"]] , dtype='float32')
    D,I = index.search(embedding , 9)
    best_matches = np.array(df["textual_representation"])[I.flatten()]
    best_matches = best_matches[1:]
    return best_matches
