# app/__init__.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {"message": "Hello DevOps!", "status": "ok"}

@app.route('/health')
def health():
    return {"status": "healthy"}, 200
