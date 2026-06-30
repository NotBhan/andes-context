# improve()

## Purpose

`improve()` enriches existing memory.

Unlike `remember()`, which stores new information, `improve()` analyzes previously stored knowledge and refines it by generating higher-quality relationships, summaries, and semantic organization.

For AndesContext, `improve()` is responsible for continuously improving project memory without requiring the repository to be re-indexed.

---

## Source

Implementation:

```
cognee/api/v1/improve/improve.py
```

Verified against repository source.

---

## Signature

```python
async def improve(
    dataset_name: str | None = None,
    **kwargs
) -> ImproveResult
```

(Note: verify exact return type against the installed Cognee version.)

---

# Improvement Pipeline

```
Existing Memory
        │
        ▼
improve()
        │
        ├── Analyze Graph
        │
        ├── Find Relationships
        │
        ├── Merge Similar Concepts
        │
        ├── Generate Better Summaries
        │
        ├── Update Knowledge Graph
        │
        └── Refresh Retrieval Quality
```

---

# What improve() Does

Typical improvement tasks include:

- enriching relationships
- refining semantic links
- generating higher-level summaries
- improving retrieval quality
- promoting session memory into permanent memory
- removing redundant information

The exact operations depend on the configured Cognee pipeline.

---

# Important Parameters

## dataset_name

Improves a single dataset.

Example:

```python
dataset_name="andes_workspace"
```

If omitted, Cognee may improve all available datasets depending on configuration.

---

# Example 1 — Improve Workspace Memory

```python
import asyncio
import cognee

async def main():
    await cognee.improve(
        dataset_name="andes_workspace"
    )

asyncio.run(main())
```

---

# Example 2 — Improve After Repository Import

```python
await cognee.remember(
    data=["./src"],
    dataset_name="andes_workspace"
)

await cognee.improve(
    dataset_name="andes_workspace"
)
```

---

# Example 3 — Improve Session Memory

```python
await cognee.remember(
    data="Authentication service is being refactored.",
    dataset_name="andes_workspace",
    session_id="editor-session"
)

await cognee.improve(
    dataset_name="andes_workspace"
)
```

---

# Example 4 — Background Improvement

```python
import asyncio

asyncio.create_task(
    cognee.improve(
        dataset_name="andes_workspace"
    )
)
```

Useful after indexing large repositories.

---

# AndesContext Usage

`improve()` should be called:

- after repository indexing
- after large documentation imports
- after multiple file updates
- when a coding session ends
- periodically during idle time

It should **not** be executed after every individual file change.

---

# Recommended Workflow

```
Repository Import
        │
        ▼
remember()
        │
        ▼
Developer Works
        │
        ▼
Session Memory
        │
        ▼
improve()
        │
        ▼
Better Permanent Memory
```

---

# Best Practices

- Batch improvements.
- Run during idle periods.
- Improve after significant changes.
- Allow session knowledge to mature before promotion.
- Avoid repeatedly improving unchanged datasets.

---

# Common Pitfalls

- Running improve() after every save.
- Improving incomplete datasets.
- Running multiple improvement jobs simultaneously.
- Expecting immediate changes after every execution.

---

# AndesContext Integration

AndesContext should schedule `improve()` automatically.

Suggested triggers:

- Repository import completed
- Session ended
- Idle for several minutes
- Manual "Optimize Memory" button
- Overnight maintenance

This allows memory quality to improve continuously without interrupting development.

---

# Related APIs

- remember()
- recall()
- forget()
- serve()

---

# Related Source Files

```
cognee/api/v1/improve/
cognee/tasks/memify/
cognee/modules/
```

---

# AndesContext Notes

`improve()` is what makes AndesContext's memory evolve.

Rather than repeatedly ingesting the same information, AndesContext should periodically refine existing knowledge so future `recall()` operations produce cleaner, more relevant Context Packages.

This operation is computationally heavier than `remember()` or `recall()` and is best treated as a background maintenance task.

