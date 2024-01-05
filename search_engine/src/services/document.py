import logging
import json
from models import document
from utils import elastic, convertText
from configs.index import stop_word

logger = logging.getLogger(__name__)
documentSchema = document.documentSchema
client = elastic.get_client()

list_stop_word = stop_word()

def check_index_exists(index_name):
    try:
        result = client.indices.exists(index=index_name)
        return result
    except Exception as e:
        logger.error(f"Error checking if index exists: {str(e)}")
        return False
    
def create_index(index_name): 
    check = check_index_exists(index_name)
    if check == True:
        client.indices.delete(index=index_name)

    result = client.indices.create(index = index_name, body = {
        "mappings": documentSchema,
    })

    return result

def add_doc(index, data):
    response = client.index(index=index, document=data)
    if response["result"] != 'created':
        return {
            "errMsg": "Something wrong when add doc"
        }
    return response

def update_doc(index, idDoc, data):
    response = client.update(index, id=idDoc, doc=data)
    return response

# def delete_doc():

def bulk_index():
    try:
        create_index("demo")
        actions = []
        with open('public/output.json', 'r') as init_data:
            data = json.load(init_data)
        
        for item in data:
            actions.append({"index": {"_index": "demo"}})
            actions.append(item)

        client.bulk(operations=actions, refresh=True)
    except Exception as e:
        return {
            "errMsg" : f"Error during bulk indexing: {str(e)}"
        }

def search_document(text, vector, similarity, top=3):
    query = {
        "index": "demo",
        "_source_excludes": ["question_vector", "answer_vector"],
        "size": top,
    }
    if text and len(vector) == 768: # hybrid
        convert_text = text
        query["query"] = {"multi_match": {
            "query": convert_text,
            "fields": ["question", "answer"],
        }}

        query["knn"] = [{
            "field": "question_vector",
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector,
            "boost": 0.6,
            "similarity": similarity
        },
        {
            "field": "answer_vector",
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector,
            "boost": 0.4,
            "similarity": similarity
        }]
    elif text and len(vector) != 768: # text only
        convert_text = text
        query["query"] = {"multi_match": {
            "query": convert_text,
            "fields": ["question", "answer"],
        }}
    elif not text and len(vector) == 768: # vector only
        query["knn"] = [{
            "field": "question_vector",
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector,
            "boost": 0.6,
            "similarity": similarity
        },
        {
            "field": "answer_vector",
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector,
            "boost": 0.4,
            "similarity": similarity
        }]

    response_data = client.search(body=query)
    hits = response_data["hits"]["hits"]

    result = []
    
    if text and vector and similarity:
        for hit in hits:
            score = hit["_score"]
            if score >= 0.5:  # can change this
                result.append({"source": hit["_source"], "score": score})
    elif text and not vector:
        result = [{"source": hit["_source"], "score": hit["_score"]} for hit in hits]
    elif not text and vector and similarity:
        result = [{"source": hit["_source"], "score": hit["_score"]} for hit in hits]

    return result
