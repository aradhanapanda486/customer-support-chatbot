# Customer Support Chatbot

This is an AI-powered customer support chatbot built with **FastAPI** for the backend and a modern HTML/CSS/JavaScript frontend. It can be used as a helpdesk assistant for answering customer queries.

## Features

- Conversational chat interface 
- FastAPI backend with session management
- Connects to a local LLM (like Ollama with phi3:mini) for intelligent responses
- Easy to deploy locally or on a cloud server

## Project Structure

```
customer-support-chatbot/
│
├── customer_service.py      # FastAPI backend
└── static/
    └── index.html           # Frontend (chat UI)
```

## Getting Started

### 1. Install Python dependencies

```bash
pip install fastapi uvicorn httpx pydantic
```

### 2. Install and Run Ollama (for local LLM)

- Download from [https://ollama.com/download](https://ollama.com/download)
- Pull a model:
  ```
  ollama pull phi3:mini
  ```
- (Ollama runs as a background service)

### 3. Start the FastAPI server

```bash
uvicorn customer_service:app --reload
```

### 4. Open the chatbot in your browser

Go to [http://localhost:8000/](http://localhost:8000/)

## Deployment

- Deploy to any cloud VM (Azure, AWS, GCP, etc.) and open ports 8000 (FastAPI) and 11434 (Ollama).
- For production, secure your endpoints and use HTTPS.

## License

This project is open source and free to use.

---
