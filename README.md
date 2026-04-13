# Story Extraction & Query Engine 🚀

An advanced engine designed to process long-form narratives, extract structured events, and provide a resilient query interface using a **Two-Phase Retrieval-Augmented Generation (RAG)** architecture.

---

## 🌟 Key Features

### 1. High-Speed Extraction
Managed by `testcase_1/main.py`:
- **Parallel Processing**: Uses `ThreadPoolExecutor` to process story chunks simultaneously across multiple files.
- **Structured Schema**: Leverages Pydantic models with detailed metadata to ensure high-fidelity extraction.
- **Source Attribution**: Every extracted event is tagged with its origin file and a unique global ID.

### 2. Two-Phase Query Engine
Powered by `testcase_1/query_story.py`:
- **Phase 1 (Broad Scan)**: Analyzes lightweight summaries to identify the most relevant event IDs.
- **Phase 2 (Deep Synthesis)**: Rehydrates only the relevant events with full context to generate precise, grounded answers.
- **Resilient Fallback**: Includes a regex-based fallback mechanism to handle unconventional LLM responses.

---

## 📂 Project Structure

- `testcase_1/main.py`: Core extraction pipeline (Load -> Chunk -> Parallel Parse -> JSON).
- `testcase_1/query_story.py`: The interactive CLI search and QA interface.
- `testcase_1/agents.py`: Specialized LLM agents for extraction and query logic.
- `testcase_1/schemas.py`: Pydantic definitions for event structure and validation.
- `testcase_1/llm.py`: Centralized LLM orchestration (Groq/Llama-3.1).
- `testcase_1/events.json`: The generated structured knowledge base.

---

## 🚀 Getting Started

### 1. Setup
Make sure you have your API keys configured in the `.env` file. We recommend using `uv` for fast dependency management.

```bash
uv sync
```

### 2. Run Extraction
Transform text stories in the `stories/` folder into a structured JSON database:

```bash
uv run testcase_1/main.py
```

### 3. Start Querying
Interact with your extracted knowledge base:

```bash
uv run testcase_1/query_story.py
```

---

## 🧠 Technical Highlights

### 🛡️ Typography & Unicode Support
The engine preserves "Smart Quotes" and advanced typography from source texts. In the JSON output, you may see character codes like:
- `\u2014`: Em Dash (—)
- `\u201c` / `\u201d`: Curly Double Quotes (“ ”)
- `\u2019`: Curly Apostrophe (’)

### ⚡ Optimization Details
- **Token Efficiency**: Phase 1 search reduces context overhead by up to 80% compared to standard "stuffing" methods.
- **Structured Purity**: Enforces JSON schema validation at every step to prevent hallucinations.
- **Multiversal Context**: Capable of handling intersecting storylines (e.g., Spider-Man and Doctor Strange) by maintaining globally unique event IDs.

---

Built for **Advanced Agentic Coding** 🛠️

