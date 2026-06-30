#!/usr/bin/env python3.13
"""AndesContext CLI entry point.

Usage:
    python3.13 -m app.cli [COMMAND]
    python3.13 andescontext.py [COMMAND]
"""

from app.cli.main import app

if __name__ == "__main__":
    app()
