#!/usr/bin/python3
""" Flask application """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """Calls close storage on teardown"""
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    """handles 404 errors and returns JSON-f 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
