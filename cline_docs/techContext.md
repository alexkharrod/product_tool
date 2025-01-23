# Technical Context

## Core Technologies
- **Python**: 3.12 (with 3.10+ compatibility layer)
- **Web Framework**: Flask 3.0
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Flask-Login 0.6
- **PDF Generation**: WeasyPrint 60.1
- **Email**: SendGrid API v3

## Development Setup
```bash
# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database initialization
flask db upgrade

# Run development server
flask run --port 8080
```

## Key Constraints
1. Must maintain Azure SQL Server 2019 compatibility
2. PDF rendering requires headless Chrome installation
3. Email templates must use MJML syntax for cross-client compatibility
4. Session cookies require HTTP-only and Secure flags

## Environment Variables
```ini
# Application
FLASK_ENV=development
FLASK_SECRET_KEY="your-secret-key-here"

# Database
SQL_SERVER="your-database-server.database.windows.net"
SQL_DATABASE="product_tool"
SQL_USER_NAME="azureuser"
SQL_PASSWORD="your-password-here"

# Email
SENDGRID_API_KEY="your-sendgrid-key"
DEFAULT_FROM_EMAIL="noreply@producttool.com"
```

## Monitoring
```mermaid
graph TD
    A[Application] --> B(Prometheus Metrics)
    A --> C(LogDNA Logging)
    A --> D(Sentry Error Tracking)
    B --> E[Grafana Dashboard]
    C --> F[Central Log Search]
    D --> G[Alert Notifications]
