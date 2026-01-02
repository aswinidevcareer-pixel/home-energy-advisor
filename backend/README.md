# Home Energy Advisor - Backend API

RESTful API for the Home Energy Advisor application, built with FastAPI following Domain-Driven Design (DDD) principles and SOLID methodology.

## Setup

1. Ollama Installation
```bash
# macOS
brew install ollama

# Start Ollama service
ollama serve

# Pull a model (in a new terminal)
ollama pull llama3.2

# run llama3.2 locally
ollama run llama3.2

```

2. Create and activate virtual environment:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the API:
   - Interactive docs: http://localhost:8000/docs
   - API: http://localhost:8000/api/v1/homes


