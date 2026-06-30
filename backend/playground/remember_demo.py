"""
remember_demo.py — Validate cognee.remember().

Purpose:
    Prove that Cognee can ingest text data into a local dataset
    using Ollama for LLM + embeddings and LanceDB/Kuzu/SQLite for storage.

Prerequisites:
    - Ollama running with phi3:mini and nomic-embed-text:latest
    - cognee installed
    - Run setup.py first (or import initialize_cognee)

Execute:
    python3.13 remember_demo.py

Expected output:
    - Confirmation that sample data was stored
    - Dataset name printed
    - No errors

Failure modes:
    - Ollama unavailable → connection refused
    - Embedding model missing → initialization error
    - LLM model missing → entity extraction fails
    - Database errors → storage path issues
    - Cognee API differences → signature mismatch
"""

import asyncio
import sys
import os

# Ensure we can import from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from setup import initialize_cognee, DATASET_NAME, run_async


SAMPLE_DATA = [
    "AndesContext is a local-first AI memory system for software development.",
    "The system uses Cognee as its persistent memory layer.",
    "Repository indexing builds long-term project memory.",
    "Context Packages are compact summaries sent to coding LLMs.",
    "The architecture separates frontend, backend, and memory layers.",
    "Ollama provides local LLM inference for entity extraction.",
    "LanceDB stores vector embeddings for semantic search.",
    "Kuzu stores the knowledge graph for structural queries.",
    "SQLite handles metadata and relational storage.",
    "The remember() function ingests data into the knowledge graph.",
]


async def main():
    print("=" * 60)
    print("  remember() Validation")
    print("=" * 60)
    print()

    # 1. Initialize
    print("[1/4] Initializing Cognee...")
    await initialize_cognee()
    print()

    # 2. Import cognee
    import cognee

    # 3. Remember sample data
    print(f"[2/4] Storing {len(SAMPLE_DATA)} items into dataset '{DATASET_NAME}'...")
    for i, item in enumerate(SAMPLE_DATA, 1):
        print(f"  [{i}/{len(SAMPLE_DATA)}] {item[:60]}...")
        try:
            result = await cognee.remember(
                data=item,
                dataset_name=DATASET_NAME,
            )
            print(f"       → OK (result type: {type(result).__name__})")
        except Exception as e:
            print(f"       → FAILED: {e}")
            # Continue with remaining items
    print()

    # 4. Verify — attempt a basic recall to confirm data exists
    print("[3/4] Verifying data was stored (basic recall)...")
    try:
        results = await cognee.recall(
            query_text="What is AndesContext?",
            datasets=[DATASET_NAME],
            top_k=3,
        )
        print(f"  Recall returned {len(results)} result(s)")
        for i, r in enumerate(results, 1):
            text = str(r)[:120]
            print(f"  [{i}] {text}")
    except Exception as e:
        print(f"  Recall verification failed: {e}")
    print()

    # 5. Summary
    print("[4/4] Summary")
    print(f"  Dataset:    {DATASET_NAME}")
    print(f"  Items sent: {len(SAMPLE_DATA)}")
    print(f"  Status:     remember() validation complete")
    print()
    print("=" * 60)
    print("  DONE — remember() validation finished")
    print("=" * 60)


if __name__ == "__main__":
    run_async(main())
