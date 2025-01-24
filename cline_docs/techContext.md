# Technical Context

## Development Environment
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate API clients
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o src/generated/
```

## API Client Generation
1. OpenAPI Spec Location: /openapi.yaml
2. Output Directory: src/generated/
3. Update Process:
   ```mermaid
   graph LR
     A[API Changes] --> B(Update openapi.yaml)
     B --> C(Regenerate Clients)
     C --> D(Commit Generated Code)
   ```

## Testing Standards
| Test Type        | Location          | Coverage Target |
|------------------|-------------------|-----------------|
| Unit Tests       | tests/unit        | ≥80%            |
| Integration      | tests/integration | ≥70%            |
| E2E              | tests/e2e         | Critical Paths  |

## CI/CD Pipeline
```bash
# Sample build script
#!/bin/zsh
flake8 application/ 
pytest --cov=application
bandit -r application/
