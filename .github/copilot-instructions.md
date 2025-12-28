# AI Watch Co-Host: Copilot Instructions

## Project Overview
AI Watch Co-Host is a FastAPI backend service that powers a live-streaming co-host assistant for watch dealers. The system classifies buyer messages and generates contextual responses using Claude AI.

## Architecture

### Core Structure
- **Backend**: FastAPI application (`app/main.py`) with two primary API endpoints
- **Models**: Pydantic schemas in `app/models/schemas.py` define all request/response contracts
- **Services**: `app/services/claude_service.py` encapsulates all Claude API interactions
- **API Routes**: Two routers under `app/api/` handle separate concerns:
  - `classify.py`: Chat message classification (type, topic, urgency)
  - `generate.py`: Response generation for specific seller context

### Data Flow
1. Client sends request with message/question + optional context
2. Route handler validates input using Pydantic schemas
3. `ClaudeService` formats prompt and calls Anthropic API
4. Claude response (JSON) is parsed and mapped to output schema
5. Response returned to client with confidence scores and reasoning

## Key Conventions

### Claude Integration Pattern
- **Prompt Design**: Always request JSON-only responses to enable reliable parsing
- **Temperature Settings**: 
  - Classification uses `temperature=0.3` (deterministic)
  - Generation uses `temperature=0.5` (creative but controlled)
- **Error Handling**: Service methods return safe default objects on failures, never raise
- **Max Tokens**: Configured in `config.py` (currently 1000), adjusted per endpoint as needed

### Schema Design
- All inputs/outputs use Pydantic `BaseModel` with explicit Field validators
- Classification schema includes confidence (0.0-1.0) and reasoning for all responses
- Product context (`ProductContext`) standardizes watch seller domain data (brand, model, price, condition)
- Seller preferences (`SellerPreferences`) control tone, length, and username inclusion

### Configuration
- Environment via `pydantic-settings` in `app/config.py`
- Default model: `claude-sonnet-4-20250514`
- CORS origins support wildcards and per-environment configuration
- All sensitive values loaded from `.env` (ANTHROPIC_API_KEY required)

## Development Workflows

### Local Setup
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Create .env with ANTHROPIC_API_KEY
# Run server
uvicorn app.main:app --reload
```

### Testing
- Tests directory exists (`backend/tests/`) but minimal initial coverage
- Use pytest with httpx for async endpoint testing
- Follow existing error handling pattern: wrap calls in try/except, return structured responses

### Running in Production
- Procfile specifies: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Deployed via nixpacks (see `nixpacks.toml`)
- Health endpoint at `/health`, API docs at `/docs`

## Common Patterns

### Adding New Endpoints
1. Define request schema in `schemas.py` (inherit `BaseModel`, use `Field` for validation)
2. Add response schema with `confidence` and `reasoning` fields
3. Create route in new/existing router under `app/api/`
4. Call `ClaudeService` method, handling exceptions by returning safe defaults
5. Include router in `main.py` with appropriate prefix

### Modifying Claude Interactions
- Edit prompt templates in `ClaudeService` methods
- Always include temperature and max_tokens parameters
- Test JSON parsing with `json.loads()` - ensure Claude output is valid JSON
- Add new response schema fields to both prompt template AND `GenerateOutput`/`ClassificationOutput`

### Critical Dependencies
- `anthropic==0.8.1`: Claude API client
- `fastapi==0.108.0` + `uvicorn`: Web framework
- `pydantic==2.5.3`: Request/response validation
- `pytest`, `pytest-asyncio`: Testing async endpoints

## Watch Seller Domain Context
The service targets watch dealers in live-streaming environments:
- Key product attributes: brand, model, year, condition, movement, box/papers
- Common buyer concerns: authenticity, pricing, specifications, condition, shipping
- Seller control: communication tone (professional/casual), response length limits
- Response validation: `requires_review` flag indicates when dealer should manually approve

## Integration Points
- Incoming messages classified as question/comment/spam with urgency levels
- Responses tagged for manual review when confidence is low
- Alternative responses field allows multiple options when applicable
- All responses include reasoning for auditability/debugging
