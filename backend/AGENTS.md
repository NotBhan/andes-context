# Purpose

Owns the backend services for AndesContext.

Responsibilities include project indexing, Cognee integration, context retrieval, and memory management.

---

# Ownership

Owns:

- CogneeService
- IndexingService
- ContextService
- Configuration
- Data Models
- Error Handling
- Logging

---

# Current Status

Milestone 1 — Backend Foundation: **Completed**
Milestone 2 — API Layer: **Completed**

Production services implemented and verified:

- CogneeService ✅
- IndexingService ✅
- ContextService ✅

API layer implemented and verified:

- Commands (health, get_backend_status, index_repository, generate_context, forget_dataset) ✅
- Schemas (Pydantic request/response models) ✅

Next: Milestone 3 — Frontend Foundation

---

# Local Contracts

Backend should remain independent from frontend implementation.

Business logic belongs here.

All Cognee interactions must go through CogneeService.

Never call `cognee.*` directly outside CogneeService.

---

# Work Guidance

Keep modules focused.

Avoid unnecessary abstractions.

Prefer composition over complex inheritance.

Use structured logging (no print statements).

Use complete Python type hints.

---

# Verification

Verify backend behavior matches project documentation.

Run playground scripts to validate Cognee integration:

```bash
cd backend/playground
python3.13 setup.py
python3.13 remember_demo.py
python3.13 recall_demo.py
python3.13 improve_demo.py
python3.13 forget_demo.py
```

---

# Child DOX Index

app/
Production backend: config, core, models, services, utils, api.

app/config/
Environment loading, provider configuration, Cognee config setup.

app/core/
Structured logging.

app/models/
Data models (RememberResult, RecallResult, ContextPackage, IndexingProgress) and error hierarchy.

app/services/
CogneeService, IndexingService, ContextService.

app/api/
API layer: async commands exposing services, Pydantic request/response schemas.

playground/
Validation scripts for Cognee integration.
