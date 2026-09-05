\# Parking\_PINFRA



This repository contains the backend for Parking\_PINFRA.



\## What I added

\- app/config.py: includes JWT settings (ACCESS\_TOKEN\_EXPIRE\_MINUTES, REFRESH\_TOKEN\_EXPIRE\_MINUTES, ALGORITHM).

\- scripts/bootstrap-env.ps1: PowerShell helper to load .env into the process environment and optionally run create\_admin.py non-interactively.

\- scripts/test-auth.ps1: PowerShell helper to test /api/auth/login and /api/auth/me.

\- .env.example: example environment variables (do not add secrets).

\- .github/workflows/ci.yml: basic CI to run tests on push/PR.

\- tests/: pytest tests for health and (optional) auth (skips if env not set).



\## Usage

1\. Copy `.env.example` to `.env` and fill in secrets.

2\. Load environment and (optionally) create the initial admin:

&#x20;  pwsh ./scripts/bootstrap-env.ps1

3\. Start the server (if not running):

&#x20;  uvicorn app.main:app --reload --port 8000

4\. Test authentication using the test script (replace credentials as needed):

&#x20;  pwsh ./scripts/test-auth.ps1 -Username admin -Password change\_me\_now



\## Tests

Run tests locally with:



&#x20;   pytest -q



The `tests/test\_auth.py` test is skipped unless `INITIAL\_ADMIN\_USERNAME` and `INITIAL\_ADMIN\_PASSWORD` are set in the environment.



\## Security

\- Do NOT commit your `.env` file to the repository. Keep SECRET\_KEY and passwords secret.




<!-- CI trigger -->
