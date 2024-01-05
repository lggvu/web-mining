from elasticsearch import Elasticsearch
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

ttl = 500
last_time = datetime.now()
client = None

def create_client():
    return Elasticsearch("http://elasticsearch:9200", timeout=30)

def get_client():
    global client, last_time

    now = datetime.now()
    current_client = client

    if not client:
        client = create_client()
    elif current_client and (now - last_time).seconds > ttl:
        last_time = now
        client = create_client()
        current_client.transport.close()
    return client
