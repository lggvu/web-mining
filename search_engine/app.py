from flask_cors import CORS
import sys
sys.path.extend(["src"])
import os

from dotenv import load_dotenv
load_dotenv()
from routes import search_api, bulk_api, add_doc_api
from flask import Flask
from argparse import ArgumentParser

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(search_api)
    app.register_blueprint(bulk_api)
    app.register_blueprint(add_doc_api)
    # app.register_blueprint(update_doc_api)
    return app


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-debug', '--debug', default=False, type=bool, help='debug mode')
    args = parser.parse_args()
    app = create_app()
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = os.environ.get("FLASK_PORT", 5007)
    print(f"Host: {host} - port: {port}")
    app.run(host=host, port=port, debug=args.debug)
