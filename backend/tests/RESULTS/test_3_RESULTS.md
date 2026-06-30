**Automated (pytest): 47/47 pass** — schemas, commands, CLI all green.

**Live Cognee Integration:**
- `setup.py` — Cognee initialized successfully with phi3:mini + nomic-embed-text
- `remember_demo.py` — Data ingested (graph nodes created), timed out during self-improvement step (known phi3:mini structured output limitation)
- `recall_demo.py` — All 4 queries returned results from the ingested dataset
- `forget_demo.py` — Dataset deleted successfully via CLI

**CLI Commands:**
- `health` — Shows ok status, Ollama reachable, Cognee initialized
- `status` — Displays full config (models, DBs, storage paths)
- `context -q "What is AndesContext?" -d andes_playground` — Generated context package with ~132 tokens
- `forget -d andes_playground` — Deleted dataset in ~6s

**Error Handling (all correct):**
- `index /nonexistent` → "Repository path does not exist"
- `context -q "  "` → "Query must not be empty"
- `forget` (no args) → "At least one of --dataset, --dataset-id, or --data-id must be provided"

**Known Limitation:** phi3:mini struggles with Cognee's structured output during the self-improvement step inside `remember()`, causing retries. The core ingestion and recall pipeline works correctly regardless.