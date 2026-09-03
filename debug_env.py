import os
import sys
import traceback

print("CWD:", os.getcwd())
print("Files in CWD:", sorted(os.listdir("."))[:50])

env_path = os.path.join(os.getcwd(), ".env")
print(".env exists:", os.path.exists(env_path))

if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        print(".env first 6 lines (masked SECRET_KEY if present):")
        for i, line in enumerate(lines[:6], start=1):
            if line.startswith("SECRET_KEY="):
                val = line.split("=", 1)[1]
                masked = (val[:4] + "..." + val[-4:]) if len(val) > 8 else ("*" * 6)
                print(f"  {i}: SECRET_KEY={masked}")
            else:
                print(f"  {i}: {line}")
    except Exception as e:
        print("Error reading .env:", e)
else:
    print(".env not found in cwd.")

print("sys.path (first 8 entries):")
for p in sys.path[:8]:
    print("  ", p)

print("\\nTrying to import app.config.settings ...")
try:
    from app.config import settings
    print("Imported app.config.settings OK")
    has_secret = getattr(settings, "SECRET_KEY", None)
    print("settings.SECRET_KEY present:", bool(has_secret))
except Exception:
    print("Failed to import app.config.settings:")
    traceback.print_exc()

print("\\nTrying to import app package ...")
try:
    import app
    print("Imported app OK, app.__file__:", getattr(app, '__file__', None))
except Exception:
    print("Failed to import app:")
    traceback.print_exc()

