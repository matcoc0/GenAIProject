# LLM Council

LLM Council is a multi-stage LLM orchestration system that leverages multiple large language models (LLMs) to provide more accurate and insightful responses to user queries. The system consists of several LLMs that first provide their individual opinions on a query, then review each other's responses, and finally a designated "Chairman" LLM compiles the final answer based on the collective insights.

Each LLM is hosted as a separate Flask API accessible via ngrok, allowing for modularity and easy swapping of models. The backend is built with FastAPI to handle asynchronous requests to the LLMs, while the frontend is developed using React and Vite for a responsive user interface.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected. The individual responses are shown in a "tab view", so that the user can inspect them all one by one.
2. **Stage 2: Review**. Each individual LLM is given the responses of the other LLMs. Under the hood, the LLM identities are anonymized so that the LLM can't play favorites when judging their outputs. The LLM is asked to rank them in accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the model's responses and compiles them into a single final answer that is presented to the user.

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure Flask API Routes

Create a `.env` file in the `llm-council/` directory with the ngrok routes of the Flask APIs:

```bash
# Flask URLs for LLM Council
CHAIRMAN_URL=https://your-chairman-url.ngrok-free.dev

DEEPSEEK_URL=https://your-deepseek-url.ngrok-free.dev
GEMMA_URL=https://your-gemma-url.ngrok-free.dev
QWEN_URL=https://your-qwen-url.ngrok-free.dev
```

## Running the Application

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
