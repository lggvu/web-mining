# web-mining
IT4868E 20231 Capstone project - Web Mining
To run this project:  
1. First, start up the Elasticsearch containers with Docker:
```
cd search_engine
docker-compose up --build
```
Now there should be three containers running concurrently: elasticsearch, kibana, and search_engine.
Run this command to bulk the data, so that we can retrieve information with Elasticsearch:
```
curl -X POST http://localhost:5007/bulk
```

2. Now we can start the live demo page. Starting from root folder:
```
cd webapp
pip install -r requirements.txt
streamlit run demo.py
```
Now you should be able to see the demo at this address: `http://localhost:8501/`.
