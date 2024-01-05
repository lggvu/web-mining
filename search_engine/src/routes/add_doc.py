from flask import Blueprint, request, jsonify
from services import document  

add_doc_api = Blueprint('add-doc', __name__)

@add_doc_api.route('/add-doc', methods=['POST'])

def add_doc_route():
    try:
        data = request.get_json()
        index = request.args.get('index')  
        if data.get('context') != None and data.get('context_vector') != None and data.get('title') != None and index != None:
            result = document.add_doc(index, data)
            return jsonify(dict(result))
        
        return jsonify({
            "errMsg": "Request missing value (context, context_vector, title, index)"
        }), 400

        
    except Exception as e:
        return jsonify({
            "error" : f"Failed to add doc {e}"
        }), 500
        