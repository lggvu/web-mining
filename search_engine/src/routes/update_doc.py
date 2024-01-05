# from flask import Blueprint, request, jsonify
# from services import document  

# update_doc_api = Blueprint('update-doc', __name__)

# @update_doc_api.route('/update-doc', methods=['POST'])

# def update_doc_route():
#     try:
#         data = request.get_json()
#         index = request.args.get('index') 
#         idDoc = request.args.get('id') 
#         # if index != None and idDoc != None

        
#     except Exception as e:
#         print(e)
#         return jsonify({
#             "error" : f"Failed to add doc {e}"
#         }), 500
        