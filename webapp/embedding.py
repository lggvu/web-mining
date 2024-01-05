'''Preprocess, word-segment and embed text'''
from sentence_transformers import SentenceTransformer
from underthesea import word_tokenize

import os

def init_model():
    model = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder')

    return model

def embedding(text, embedding_model):
    """
    input: raw, unsegmented text
    output: embedding using Bi-encoder
    """
    # segmented_text = rdrsegmenter.word_segment(text)
    segmented_text = word_tokenize(text, format="text")
    embeddings = embedding_model.encode(segmented_text)

    return embeddings.tolist()
