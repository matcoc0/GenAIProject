# GenAIProject

1. Change the `OLLAMA_BASE_URL` and `MODEL_NAME` variables in the `settings.py` file to match your local Ollama server configuration.

2. Start the Flask API by running the `api.py` file:

   ```bash
   python api.py
   ```

3. Use `ngrok` to expose your local server to the internet:

   ```bash
   ngrok http 5000
   ```