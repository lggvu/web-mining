from flask import Blueprint, request, jsonify
from services import document  

bulk_api = Blueprint('bulk', __name__)

@bulk_api.route('/bulk', methods=['POST'])

def bulk_index_route():
    try:
        result = document.bulk_index()
        if result and result["errMsg"]:
            return jsonify({
                "errMsg": result["errMsg"]
            }), 400
        return jsonify({
            "msg": "Bulk index data successfully"
        })
    except Exception as e:
        return jsonify({
            "error" : "Internal Server Error"
        }), 500
    