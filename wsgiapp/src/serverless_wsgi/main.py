# coding: utf-8

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return jsonify({'message': 'Hello serverless WSGI world!!'})


@app.route('/<path:path>')
def any_path(path):
    return jsonify({'message': 'Here: /{}'.format(path)})


if __name__ == '__main__':
    app.run()
