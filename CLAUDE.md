# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GmailWrapper is a Python module for interacting with the Gmail API using modern async/httpx patterns. The main API class is `GmailAPICaller` which provides comprehensive Gmail operations including sending, reading, searching, and managing emails, drafts, and labels.

## Development Commands

### Linting and Code Quality
```bash
# Run full linting suite (Black, isort, ruff, pre-commit)
bin\linting.bat

# Individual tools
black gmail_wrapper\
isort --atomic gmail_wrapper\
ruff check .
```

### Dependency Management
```bash
# Update Python dependencies using uv
bin\py_update.bat
```

### Git Operations  
```bash
# Interactive commit and push helper
bin\git_update.bat [branch] [commit_message]
```

## Project Structure

- `gmail_wrapper/api.py` - Main `GmailAPICaller` class with async Gmail API operations
- `gmail_wrapper/consts.py` - Configuration constants and file paths
- `bin/` - Development utility batch scripts for Windows
- Core dependencies managed via `core_requirements.in/.txt`
- Dev dependencies managed via `dev_requirements.in/.txt` 

## Key Architecture

### GmailAPICaller Class
- Uses httpx.AsyncClient for HTTP requests to Gmail API
- Handles OAuth2 authentication with token refresh
- Supports switching between endpoints: threads, messages, drafts
- Provides CRUD operations for all Gmail resources
- Uses environment variables for configuration (BACKEND_DIR, FLOW_PORT, etc.)

### Authentication Flow
- Credentials stored at `{BACKEND_DIR}/credentials.json` 
- Tokens cached at `{BACKEND_DIR}/token.json`
- OAuth flow runs on configurable port (default 5000)
- Required scopes: gmail.send, gmail.compose, gmail.modify

### Code Quality Tools
- Black formatter (line length: 80)
- isort with Black profile
- Ruff linter (E, F, B rules)
- pre-commit hooks
- Python 3.10+ target versions

## Environment Variables

- `BACKEND_DIR` - Directory for credentials/tokens (default: "./backend")
- `FLOW_PORT` - OAuth flow port (default: 5000)  
- `EMAIL_SIGNATURE` - Default email signature
- `HTTP_PROXY` - Optional proxy URL for requests

## Testing

No specific test framework is configured. Check with maintainer for testing approach before adding tests.