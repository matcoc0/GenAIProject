# GenAI Project - LLM Council System

<ins>CDOF2 - Team members:</ins>
- Mathieu COWAN
- Julien DE VOS
- Eliott COUTAZ
- Sacha CROCHET
- Adrien DE MAILLY NESLE

This project implements a multi-stage LLM orchestration system that leverages multiple large language models to provide more accurate and insightful responses through collaborative deliberation. The system consists of two main components: the **LLM Council** application and the **LLM Flask API** wrappers.

## Overview

The LLM Council system operates through a three-stage process:

1. **Stage 1: First Opinions** - Multiple LLMs independently provide their responses to a user query
2. **Stage 2: Review** - Each LLM reviews and ranks the responses from other LLMs (anonymized to prevent bias)
3. **Stage 3: Final Response** - A designated "Chairman" LLM compiles all insights into a single, comprehensive answer

## Project Structure

```
GenAIProject/
├── llm-council/          # Main orchestration application (FastAPI + React)
│   ├── backend/          # FastAPI backend for coordinating LLMs
│   ├── frontend/         # React + Vite frontend interface
│   └── data/             # Conversation storage
│
└── llm-flask-api/        # Flask API wrapper for local Ollama models
    └── app.py            # Flask server exposing LLM endpoints
```

### Component Details

#### LLM Council (`llm-council/`)
The main application that orchestrates the multi-stage LLM deliberation process.

This application is a fork of the original [llm-council](https://github.com/karpathy/llm-council) project, modified to interface with local Ollama LLM servers via the Flask API wrappers.

- **Backend:** FastAPI with async httpx for concurrent LLM requests
- **Frontend:** React + Vite with responsive UI for viewing responses
- **Storage:** JSON-based conversation persistence
- **Package Management:** uv for Python dependencies

See [llm-council/README.md](llm-council/README.md) for detailed setup and usage.

#### LLM Flask API (`llm-flask-api/`)
Simple Flask API wrappers that serve as intermediaries between the Council and local Ollama LLM servers.

- **Purpose:** Expose local Ollama models via HTTP endpoints
- **Deployment:** Run locally and expose via ngrok for external access
- **Configuration:** Environment-based model selection

See [llm-flask-api/README.md](llm-flask-api/README.md) for detailed setup and usage.

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js and npm
- [uv](https://docs.astral.sh/uv/) package manager
- **Either:**
  - [Docker](https://www.docker.com/) and Docker Compose (recommended for running LLM APIs)
  - **Or:** [Ollama](https://ollama.ai/) installed and running locally
- [ngrok](https://ngrok.com/) for exposing local APIs (included in Docker setup)

### Setup Steps

1. **Set up Flask APIs for each LLM**

   You can run the Flask API wrappers either with Docker (recommended) or locally.

   **Option A: Using Docker (Recommended)**
   
   For each model you want to use (e.g., DeepSeek, Gemma, Qwen, Chairman):
   
   ```bash
   cd llm-flask-api
   
   # Edit docker-compose.yml and set MODEL_NAME to your desired model
   # Then start all services (Ollama + Flask API + ngrok)
   docker-compose up -d
   
   # Pull the Ollama model
   docker exec -it ollama_backend ollama pull your-model-name
   
   # Get the ngrok URL from http://localhost:4040
   ```
   
   To run multiple models, you'll need to:
   - Create separate directories or modify the docker-compose.yml to run on different ports
   - Use different ngrok tunnels for each instance
   
   **Option B: Using Local Python Installation**
   
   For each model you want to use:
   
   ```bash
   cd llm-flask-api
   
   # Create .env file
   echo "OLLAMA_BASE_URL=http://localhost:11434" > .env
   echo "MODEL_NAME=your-model-name" >> .env
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the Flask API
   python app.py
   
   # In another terminal, expose with ngrok
   ngrok http 5000
   ```
   
   Repeat this process for each LLM, running each on a different port and exposing each with ngrok.

2. **Configure the LLM Council**

   ```bash
   cd llm-council
   
   # Create .env file with ngrok URLs
   cat > .env << EOF
   CHAIRMAN_URL=https://your-chairman-url.ngrok-free.dev
   DEEPSEEK_URL=https://your-deepseek-url.ngrok-free.dev
   GEMMA_URL=https://your-gemma-url.ngrok-free.dev
   QWEN_URL=https://your-qwen-url.ngrok-free.dev
   EOF
   
   # Install backend dependencies
   uv sync
   
   # Install frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

3. **Run the LLM Council**

   Option 1 - Use the start script:
   ```bash
   cd llm-council
   ./start.sh
   ```
   
   Option 2 - Run manually:
   ```bash
   # Terminal 1: Backend
   cd llm-council
   uv run python -m backend.main
   
   # Terminal 2: Frontend
   cd llm-council/frontend
   npm run dev
   ```

4. **Access the application**

   Open http://localhost:5173 in your browser

## Tech Stack

- **Frontend:** React, Vite, react-markdown
- **Backend:** FastAPI (Python 3.10+), async httpx
- **LLM APIs:** Flask, Ollama
- **Tunneling:** ngrok
- **Package Management:** uv (Python), npm (JavaScript)