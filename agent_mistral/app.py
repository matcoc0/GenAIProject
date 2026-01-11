from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID", "unknown_agent")
MODEL_NAME = os.getenv("MODEL_NAME", "unknown_model")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.0")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "agent_id": AGENT_ID,
        "model": MODEL_NAME,
        "version": SERVICE_VERSION
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
