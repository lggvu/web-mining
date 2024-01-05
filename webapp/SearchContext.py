import os

from dotenv import load_dotenv
load_dotenv()
import requests

from embedding import *

def get_response(text='', vector=[], similarity=0, top=3):
    print("searching...")
    API_SEARCH_ENGINE = f"{os.environ['URL_SEARCH']}/search"
    payload = {
        "text": text,
        "vector": vector,
        "similarity": similarity,
        "top": top,
    }
    response = requests.post(API_SEARCH_ENGINE, json=payload)
    return response.json()


def search(question, embedding_model, search_type="hybrid", threshold=.5, top=3):
    context = ""

    if search_type == "vector" or search_type == None:
        print("searching mode: vector")
        embedded_text = embedding(question, embedding_model)
        context = get_response(vector=embedded_text, similarity=threshold, top=top)

    elif search_type == "text":
        print("searching mode: text")
        context = get_response(text=question)
    
    elif search_type == "hybrid":
        print("search mode: hybrid")
        embedded_text = embedding(question, embedding_model)
        context = get_response(text=question, vector=embedded_text, similarity=threshold, top=top)
    # print("retrieved context: ", context)
    return context

if __name__ == "__main__":
    embedding_model = init_model()
    question = "laptop lenovo dưới 20 triệu"
    context = search(question, embedding_model, search_type="hybrid", top=3)

    print(context)
