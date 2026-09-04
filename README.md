# Parking_PINFRA

This repository contains the backend for Parking_PINFRA.

## What I added
- app/config.py: includes JWT settings (ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM).
- scripts/bootstrap-env.ps1: PowerShell helper to load .env into the process environment and optionally run create_admin.py non-interactively.
- scripts/test-auth.ps1: PowerShell helper to test /api/auth/login and /api/auth/me.

## Usage
1. Load environment and (optionally) create the initial admin:
   pwsh ./scripts/bootstrap-env.ps1

2. Start the server (if not running):
   uvicorn app.main:app --reload --port 8000

3. Test authentication using the test script (replace credentials as needed):
   pwsh ./scripts/test-auth.ps1 -Username admin -Password change_me_now

## Security
- Do NOT commit your .env file to a public repository.
- Keep SECRET_KEY and passwords secret.

