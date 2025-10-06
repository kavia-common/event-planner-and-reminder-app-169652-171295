import json
from pathlib import Path

from fastapi.testclient import TestClient

from .main import app


def main():
    # Initialize app routes and ensure startup is executed
    with TestClient(app) as _client:
        _client.get("/")  # trigger route and startup
    # Access the OpenAPI schema
    openapi = app.openapi()
    out_path = Path(__file__).resolve().parents[2] / "interfaces" / "openapi.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(openapi, indent=2))
    print(f"OpenAPI schema written to: {out_path}")


if __name__ == "__main__":
    main()
