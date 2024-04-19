from flask import Flask
from flask import Flask, jsonify
from jinja2 import escape

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def home():
    return "<h1>Hello</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)