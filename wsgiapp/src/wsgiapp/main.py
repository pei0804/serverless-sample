# coding: utf-8

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'Hello serverless WSGI world!!'})
