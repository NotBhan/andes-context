# Purpose

Owns the backend services for AndesContext.

Responsibilities include project indexing, Cognee integration, context retrieval, LLM communication and memory management.

---

# Ownership

Owns:

- Context Engine
- Cognee Integration
- Project Indexing
- Memory Operations
- Backend APIs

---

# Local Contracts

Backend should remain independent from frontend implementation.

Business logic belongs here.

---

# Work Guidance

Keep modules focused.

Avoid unnecessary abstractions.

Prefer composition over complex inheritance.

---

# Verification

Verify backend behavior matches project documentation.

---

# Child DOX Index

app/
Production backend: config, core, models, services, utils.

playground/
Validation scripts for Cognee integration.
