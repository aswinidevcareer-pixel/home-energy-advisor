# 🏠 Home Energy Advisor

A full-stack web application that provides AI-powered, personalized energy efficiency recommendations for homes using Large Language Models (LLMs).

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Local Ollama using https://ollama.com/**

### 1. Installation

#### 1.1 Ollama Installation
```bash
# macOS
brew install ollama

# Start Ollama service
ollama serve

# Pull a model (in a new terminal)
ollama pull llama3.2

```

#### 1.2 Clone and Setup application

```bash
cd home-energy-advisor

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Database Setup

The SQLite database is **automatically initialized** when you first start the backend server. No manual setup required!

- **Database file**: `backend/home_energy_advisor.db`
- **Auto-creation**: Tables are created on startup via SQLAlchemy migrations
- **Schema**: Defined in `backend/app/infrastructure/database.py`

The database will be created with the `homes` table containing all necessary fields for home profiles.

### 3. Run the Application

**Option A: Start Everything at Once**
```bash
chmod +x start-all.sh
./start-all.sh
```

**Option B: Start Services Separately**

Terminal 1 - Backend:
```bash
cd backend
chmod +x start.sh
./start.sh
# Database is automatically initialized on first startup
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## 🤖 AI Tool Usage Log

### Tools Used
- **GitHub Copilot** - Primary AI coding assistant used throughout the project

### Development Approach

#### What AI Was Used For:
1. **Backend API** - Generated the initial FastAPI boilerplate with proper DDD (Domain-Driven Design) architecture
   - Domain entities, repositories, and services following SOLID principles
   - SQLAlchemy models and database configuration
   - OpenAPI-compliant REST endpoints with proper validation

2. **LLM Integration Layer** - Created the provider abstraction layer
   - Strategy pattern implementation for multi-provider support (Ollama, OpenAI, Anthropic)
   - Factory pattern for provider instantiation
   - Prompt engineering templates for energy advice generation

3. **Frontend Vue Components** - Generated the basic form structure and API integration
   - TypeScript interfaces for type safety
   - Async API calls with proper error handling
   - Reactive state management

#### Effective Prompts Used:

**Prompt 1: Architecture Design**
```
"Build a RESTful API for the Home Energy Advisor with these requirements:
- Use SQLite for database
- Follow DDD and SOLID principles
- Design models using domain-driven design
- Use FastAPI with OpenAPI standards
- Add proper validation for API endpoints"
```
This generated a well-structured backend with clear separation of concerns (domain, application, infrastructure layers).

**Prompt 2: Flexible LLM Integration**
```
"Create an LLM integration that works with any provider.
Use strategy pattern and best practices. Make it easy to add new providers."
```
This produced a clean abstraction layer with `LLMProvider` interface, concrete implementations, and a factory pattern.

#### What I Designed/Wrote Myself:

1. **Architecture & Design Patterns** - Made strategic decisions on which design patterns to apply and where:
   - Repository Pattern for data access abstraction
   - Factory Pattern for LLM provider instantiation
   - Builder Pattern for complex prompt construction
   - Strategy Pattern for multi-provider LLM support
   - Dependency Injection throughout the application layers
   - Clean Architecture with clear separation between domain, application, infrastructure, and API layers
2. **Domain Model Design** - Decided on the home profile attributes based on real energy audit considerations.
3. **Prompt Engineering Strategy** - Crafted the LLM prompt structure.
4. **API Error Handling Strategy** - Designed the error response patterns
5. **Project Structure** - Organized the repository layout
6. **Schema Enforcement Strategy** - Decided on the multi-layered validation approach with provider-specific implementations

#### What AI Got Wrong (and How I Fixed It):

**Issue 1: Schema Enforcement for LLM Responses**
```
"The LLM responses need strict schema enforcement. Implement JSON schema validation
across all providers to ensure type safety and required fields. Use OpenAI's native
structured outputs where possible, and enhance prompts for other providers."
```
This created a robust multi-layered validation system:
- Defined a strict schema for LLM response.
- Updated the LLM provider to enforce schema

**Issue 2: Missing Production-Grade Retry Logic**

**What Happened:**
AI initially implemented manual retry logic with basic exponential backoff, but I identified that this approach wasn't following production best practices. Python has established libraries like `tenacity` specifically designed for this purpose.

**The Fix:**
I adjusted the code to use the `tenacity` library across all LLM providers:
```python
# Added to requirements.txt:
tenacity>=8.2.0

# Refactored the provider to use:
@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
```

This provides:
- Declarative retry policies
- Exponential backoff with configurable limits
- Automatic logging of retry attempts
- Production-tested reliability
- Cleaner, more maintainable code

**Issue 3: Frontend - Refactored to feature-based architecture:**
```
frontend/src/
├── components/
│   ├── common/         # LoadingSpinner
│   ├── home/          # HomeProfileForm
│   └── advice/        # AdviceResults, RecommendationCard
├── composables/       # useEnergyAdvice (business logic)
├── services/api/      # client, homeApi, adviceApi
└── utils/            # formatters
```

**Issue 4: Simplified UI Styling**
```
"Simplify the styles for the UI - make them minimal, clean, and easy to maintain"
```

