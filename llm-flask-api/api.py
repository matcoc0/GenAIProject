from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2:1b')

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

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
        
        # Optional parameters
        if 'options' in data:
            ollama_payload['options'] = data['options']
        
        # Call Ollama API
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/chat',
            json=ollama_payload,
            timeout=120
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
    print(f"Using Ollama at: {OLLAMA_BASE_URL}")
    print(f"Default model: {MODEL_NAME}")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
