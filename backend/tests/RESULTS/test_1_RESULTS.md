# Cognee Integration Validation Report

### 1. Files Created

```
backend/playground/
    setup.py              — Bootstrap configuration
    remember_demo.py      — remember() validation
    recall_demo.py        — recall() validation
    improve_demo.py       — improve() validation
    forget_demo.py        — forget() validation
```

### 2. How to Execute

All scripts require **Python 3.13** (cognee 1.2.2 is installed for 3.13):

```bash
cd backend/playground
/usr/bin/python3.13 setup.py
/usr/bin/python3.13 remember_demo.py
/usr/bin/python3.13 recall_demo.py
/usr/bin/python3.13 improve_demo.py
/usr/bin/python3.13 forget_demo.py
```

Scripts must be run in order: `remember_demo.py` first (populates data), then the others.

### 3. Expected Output

- **setup.py**: Prints config summary, "Cognee initialized successfully"
- **remember_demo.py**: 10 items stored with `RememberResult`, recall returns results
- **recall_demo.py**: 4 queries return `graph_completion` results with relevant text
- **improve_demo.py**: `improve()` completes, recall still returns results
- **forget_demo.py**: `forget()` completes, recall returns fewer/no results

### 4. Cognee Limitations Discovered

| Issue | Details |
|-------|---------|
| **HuggingFace tokenizer dependency** | OllamaEmbeddingEngine requires a `HUGGINGFACE_TOKENIZER` env var pointing to a valid HF model (`nomic-ai/nomic-embed-text-v1`). Without it, embedding fails with `None is not a valid model identifier`. |
| **`transformers` + PyTorch required** | Even though embeddings run through Ollama, the tokenizer loading requires `transformers`. PyTorch is not installed so only tokenizer utilities work. |
| **qwen3.5:4b thinking mode** | Thinking-mode models exhaust `max_tokens` on reasoning before producing structured output. **phi3:mini** works but is slower for structured output tasks. |
| **Slow structured output retries** | `recall()` triggers `SessionTurnAnalysis` structured output which retries on validation failures. With phi3:mini this adds significant latency. Setting `CACHING=false` disables session memory. |
| **Connection test timeout** | `COGNEE_SKIP_CONNECTION_TEST=true` is needed to avoid 30s timeouts on first run. |

### 5. API Differences from Documentation

| Function | Documented | Actual (v1.2.2) |
|----------|-----------|-----------------|
| `remember()` | `dataset_name` param | `dataset_name` param — **matches** |
| `recall()` | `query_text`, `datasets` params | `query_text`, `datasets` params — **matches** |
| `improve()` | `dataset_name` param | `dataset` param (string or UUID) — **different** |
| `forget()` | `dataset_name`, `document_id` params | `dataset` (str), `dataset_id` (UUID), `data_id` (UUID) — **different** |

### 6. Recommendations for Production Integration

1. **Use `phi3:mini` or larger non-thinking models** for Cognee's LLM. Thinking-mode models (qwen3.5) cause structured output failures.

2. **Set these env vars in production**:
   ```
   HUGGINGFACE_TOKENIZER=nomic-ai/nomic-embed-text-v1
   CACHING=false  (until session memory is needed)
   COGNEE_SKIP_CONNECTION_TEST=true  (for startup speed)
   ENABLE_BACKEND_ACCESS_CONTROL=false  (local-only)
   ```

3. **Use correct API params**: `improve(dataset=...)` not `dataset_name`. `forget(dataset=...)` not `dataset_name`.

4. **Remember is slow** (~30s per item with phi3:mini due to LLM calls for entity extraction). Batch ingestion is recommended.

5. **Recall uses hybrid search** (vector + graph) and returns `RecallResponse` objects with `.text`, `.search_type`, `.score`, `.dataset_name` attributes.

6. **Database directories**: `.cognee_data/` and `.cognee_system/` should be gitignored and placed in the backend directory.