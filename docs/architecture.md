# Architecture and tradeoffs

Classifier -> knowledge or order tool or handoff -> ticket persistence

The bearer-token mapping is resolved server-side before domain access. Every persisted record carries its workspace. SQL values are parameterized. SQLite WAL supports a small local workload; this is not a scale benchmark.

Implemented graph nodes and routing, constrained read tool, handoff persistence and policy/permission evaluation.

## Boundaries

Routing is a deterministic baseline, not an LLM decision maker. There is no automatic refund, external communication, PostgreSQL deployment or React support console. Human handoff creates a pending ticket; it does not contact an agent. Each request is one graph run; no conversational checkpointing is claimed.

## Interview walkthrough

Follow one request from app.py through the domain module to persistence. Explain the test that prevents cross-workspace access, the main failure mode, and the change needed for production traffic. Separate recreated career context from present implementation work.
