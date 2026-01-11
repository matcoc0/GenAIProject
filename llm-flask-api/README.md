# LLM Flask API

This repository contains a simple Flask API that serves as a wrapper around a local Ollama LLM server. It exposes endpoints to generate text completions using specified models hosted on the Ollama server.

## Setup Options

You can run this API using either Docker (recommended) or a local Python installation.

### Option 1: Docker Setup (Recommended)

This option uses Docker Compose to run Ollama, the Flask API, and ngrok in containers.

#### Prerequisites
- Docker and Docker Compose installed
- ngrok account (for tunneling)
- python 3.11 or higher
- requirements file, api.py, docker-compose and DockerFile in a same folder

#### Steps

1. **Configure the model:**
   
   Edit the `docker-compose.yml` file and change the `MODEL_NAME` environment variable to your desired Ollama model:
   
   ```yaml
   environment:
     - MODEL_NAME=llama3.2:1b # Change to your model
   ```

2. **(Optional) Set up ngrok authentication:**
   
   If you want to use ngrok, set your authtoken as an environment variable:
   
   ```bash
   export NGROK_AUTHTOKEN=your_ngrok_authtoken
   ```
   
   Or add it to a `.env` file in the project root.

3. **Start all services:**
   
   ```bash
   docker compose up --build -d
   ```
   
   This will start:
   - Ollama server on port 11434
   - Flask API on port 5000
   - ngrok tunnel (accessible at http://localhost:4040 for inspection)

4. **Pull the Ollama model if there is any problem with the automation:**
   
   ```bash
   docker exec -it ollama_backend ollama pull llama3.2:1b
   ```
   
   Replace `llama3.2:1b` with your desired model.

5. **Get your ngrok URL:**
   
   Visit http://localhost:4040 to see your ngrok public URL, or check the logs:
   
   ```bash
   docker logs -f flask_llm_api
   ```
   or
   ```bash
   docker logs ngrok_tunnel
   ```

#### GPU Support

If you have an NVIDIA GPU, uncomment the GPU section in `docker-compose.yml`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

#### Stopping the Services

```bash
docker compose down
```

To also remove the Ollama storage volume:

```bash
docker compose down -v
```

### Option 2: Local Python Setup

#### 1. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

#### 2. Configure Ollama Server

Create a `.env` file in the project root with the following content:
```bash
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=your-ollama-model-name
```

#### 3. Running the Flask API

1. Start the Flask API by running the `api.py` file:

   ```bash
   python api.py
   ```

2. Use `ngrok` to expose your local server to the internet:

   ```bash
   ngrok http 5000
   ```
