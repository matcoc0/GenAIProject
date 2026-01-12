from flask import Flask, request, jsonify
import requests
import os
import time
import threading
from dotenv import load_dotenv

load_dotenv()

# Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2:1b') # change model if no model have been chosen
NGROK_API_URL = "http://localhost:4040/api/tunnels"

app = Flask(__name__)

# --- AUTOMATION FUNCTIONS ---

def ensure_model_exists():
    """Checks if the model exists, if not, triggers a pull."""
    print(f"[*] Checking if model '{MODEL_NAME}' is available...")
    
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags')
        if response.status_code == 200:
            installed_models = [m['name'] for m in response.json().get('models', [])]
            
            if any(MODEL_NAME in m for m in installed_models):
                print(f"[+] Model '{MODEL_NAME}' is ready!")
                return
            
        print(f"[-] Model '{MODEL_NAME}' not found. Starting automatic pull... (This may take a while)")
        
     
        pull_resp = requests.post(
            f'{OLLAMA_BASE_URL}/api/pull', 
            json={'name': MODEL_NAME}, 
            stream=True
        )
        
        for line in pull_resp.iter_lines():
            if line:
                print(f"    Pulling... {line.decode('utf-8')[-50:]}") # Print last 50 chars 
        
        print(f"[+] Successfully pulled '{MODEL_NAME}'!")

    except Exception as e:
        print(f"[!] Error managing model: {e}")

def display_ngrok_url():
    """Polls the Ngrok API to find the public URL."""
    print("[*] Waiting for Ngrok tunnel...")
    time.sleep(3)
    
    try:
        response = requests.get(NGROK_API_URL, timeout=5)
        if response.status_code == 200:
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    public_url = tunnel.get('public_url')
                    print("\n" + "="*50)
                    print(f" ACCESS URL FOR MASTER PC: {public_url}")
                    print("="*50 + "\n")
                    return
        print("[!] Could not find active Ngrok tunnel.")
    except Exception as e:
        print(f"[!] Error fetching Ngrok URL: {e}")
        print("    (Make sure the ngrok service is named 'ngrok' in docker-compose)")

# --- FLASK ROUTES ---

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model': MODEL_NAME}), 200

@app.route('/info', methods=['GET'])
def get_node_info():
    return jsonify({
        "status": "online",
        "node_id": os.getenv('HOSTNAME', 'unknown-node'),
        "role": "Logic/Reasoning",
        "model": MODEL_NAME
    }), 200

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat with Ollama API
    Expected JSON body:
    {
        "messages": [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "model": "optional-model-name",  # Optional, uses MODEL_NAME if not provided
        "stream": false  # Optional, default is false
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing messages in request body'}), 400
        
        messages = data['messages']
        model = data.get('model', MODEL_NAME)
        stream = data.get('stream', False)
        
        # Prepare request to Ollama
        ollama_payload = {
            'model': model,
            'messages': messages,
            'stream': stream
        }
        
        if 'options' in data:
            ollama_payload['options'] = data['options']
        
        # Call Ollama API
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/chat',
            json=ollama_payload,
            timeout=460
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                'error': 'Ollama API error',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to connect to Ollama API',
            'details': str(e)
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/models', methods=['GET'])
def list_models():
    """List available models from Ollama"""
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                'error': 'Failed to fetch models',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to connect to Ollama API',
            'details': str(e)
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


if __name__ == '__main__':

    setup_thread = threading.Thread(target=lambda: (ensure_model_exists(), display_ngrok_url()))
    setup_thread.start()
    
    print(f"Starting Flask API on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
