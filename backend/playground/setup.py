"""
setup.py — Cognee playground bootstrap.

Purpose:
    Centralizes Cognee configuration for the validation playground scripts.
    Every demo script imports initialize_cognee() from this module.

Prerequisites:
    - Ollama running on localhost:11434
    - Models pulled: phi3:mini, nomic-embed-text:latest
    - cognee installed (pip install cognee)
    - kuzu installed (bundled with cognee)

Usage:
    from setup import initialize_cognee, DATASET_NAME

    await initialize_cognee()

Expected output:
    "Cognee initialized successfully"

Failure modes:
    - Ollama not running → connection refused
    - Model missing → model not found error
    - Database lock → another process using the same DB path
"""

import os
import sys
import asyncio
import socket
from pathlib import Path

# ── Dataset name used across all playground scripts ──
DATASET_NAME = "andes_playground"

# ── Data directories (project-local, not global) ──
DATA_ROOT = Path(__file__).resolve().parent.parent / ".cognee_data"
SYSTEM_ROOT = Path(__file__).resolve().parent.parent / ".cognee_system"


def _check_ollama(host: str = "localhost", port: int = 11434) -> bool:
    """Return True if Ollama is reachable."""
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except (ConnectionRefusedError, OSError):
        return False


def _set_environment():
    """Configure environment variables for Cognee before import."""
    os.environ.setdefault("LLM_PROVIDER", "ollama")
    os.environ.setdefault("LLM_MODEL", "phi3:mini")
    os.environ.setdefault("LLM_ENDPOINT", "http://localhost:11434/v1")
    os.environ.setdefault("LLM_API_KEY", "ollama")

    os.environ.setdefault("EMBEDDING_PROVIDER", "ollama")
    os.environ.setdefault("EMBEDDING_MODEL", "nomic-embed-text:latest")
    os.environ.setdefault("EMBEDDING_ENDPOINT", "http://localhost:11434/api/embed")
    os.environ.setdefault("EMBEDDING_API_KEY", "ollama")
    os.environ.setdefault("EMBEDDING_DIMENSIONS", "768")

    # HuggingFace tokenizer for Ollama embedding engine token counting
    os.environ.setdefault("HUGGINGFACE_TOKENIZER", "nomic-ai/nomic-embed-text-v1")

    os.environ.setdefault("VECTOR_DB_PROVIDER", "lancedb")
    os.environ.setdefault("GRAPH_DB_PROVIDER", "kuzu")
    os.environ.setdefault("RELATIONAL_DB_PROVIDER", "sqlite")

    os.environ.setdefault("DATA_ROOT_DIRECTORY", str(DATA_ROOT))
    os.environ.setdefault("SYSTEM_ROOT_DIRECTORY", str(SYSTEM_ROOT))

    # Disable multi-user access control for local playground
    os.environ.setdefault("ENABLE_BACKEND_ACCESS_CONTROL", "false")

    # Disable session memory to avoid slow LLM-based session turn analysis
    os.environ.setdefault("CACHING", "false")

    # Skip slow connection tests during validation
    os.environ.setdefault("COGNEE_SKIP_CONNECTION_TEST", "true")


async def initialize_cognee() -> None:
    """
    Initialize Cognee with local Ollama + LanceDB + Kuzu + SQLite.

    Raises:
        SystemExit: if Ollama is unreachable or cognee import fails.
    """
    # 1. Pre-flight: Ollama
    if not _check_ollama():
        print("ERROR: Ollama is not reachable at localhost:11434")
        print("       Start it with: ollama serve")
        sys.exit(1)

    # 2. Set env vars
    _set_environment()

    # 3. Import cognee (after env is configured)
    try:
        import cognee
    except ImportError:
        print("ERROR: cognee is not installed.")
        print("       Install with: pip install cognee")
        sys.exit(1)

    # 4. Print config summary
    print(f"  LLM provider:     {os.environ['LLM_PROVIDER']}")
    print(f"  LLM model:        {os.environ['LLM_MODEL']}")
    print(f"  Embedding model:  {os.environ['EMBEDDING_MODEL']}")
    print(f"  Vector DB:        {os.environ['VECTOR_DB_PROVIDER']}")
    print(f"  Graph DB:         {os.environ['GRAPH_DB_PROVIDER']}")
    print(f"  Relational DB:    {os.environ['RELATIONAL_DB_PROVIDER']}")
    print(f"  Data root:        {DATA_ROOT}")
    print(f"  System root:      {SYSTEM_ROOT}")

    # 5. Verify cognee can be imported without errors
    print("  cognee version:   ", cognee.__version__)
    print()
    print("Cognee initialized successfully.")


def run_async(coro):
    """Helper to run an async function from a sync script."""
    asyncio.run(coro)


if __name__ == "__main__":
    run_async(initialize_cognee())
