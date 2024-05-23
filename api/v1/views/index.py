#!/usr/bin/python3
"""module that returns json status ok"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a json status ok"""
    return jsonify({"status": "OK"})
