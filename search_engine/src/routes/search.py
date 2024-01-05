from flask import Blueprint, request, jsonify
from services import document  

search_api = Blueprint('search', __name__)

@search_api.route('/search', methods=['POST'])

def search_document_route():
    try:
        data = request.get_json()
        text = data.get('text')
        vector = data.get('vector')  
        similarity = data.get('similarity')
        top = data.get('top')
    
        result = document.search_document(text, vector, similarity, top)
        # result = document.bulk_search()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({
            "error" : "Failed to create query"
        }), 500
    