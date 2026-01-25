from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Welcome to DevOps Project API",
        "hostname": socket.gethostname(),
        "status": "operational"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
