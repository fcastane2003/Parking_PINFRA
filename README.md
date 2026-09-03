name=README.md
Repositorio: Parking_PINFRA

Responsabilidad:
- Contiene el código del backend del Sistema de Gestión de Estacionamiento y Reconocimiento de Placas (Parking PINFRA).
- Scaffold inicial: FastAPI, utilidades, y configuración mínima.
- Sprint 0: inicializar estructura del proyecto, tests básicos y CI.

Instrucciones rápidas:
1. Abrir este repo en GitHub Codespaces (recomendado).
2. Crear un entorno virtual y activar (Windows PowerShell):
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
3. Ejecutar servidor de desarrollo:
   uvicorn app.main:app --reload --port 8000

Reglas de entrega:
- Cada archivo entregado debe ser completo y con la ruta exacta.
- No se incluirán secretos en el repo.
- El código pasa por linters/formateadores antes de entregar (black/isort/flake8).

Notas:
- Para desarrollo local sin admin usamos SQLite por defecto (DATABASE_URL en .env).
- Para desarrollo completo (Postgres + Redis + Codespaces) sigue las instrucciones en docs/ cuando estén disponibles.