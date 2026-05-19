"""Compatibility FastAPI entrypoint.

Allows running both:
- uvicorn main:app --reload
- uvicorn app.main:app --reload
"""

from main import app

__all__ = ["app"]
