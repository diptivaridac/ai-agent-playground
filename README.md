# 🤖 AI Agent Playground

A multi-tool agentic system built with the Anthropic Claude API — designed to explore how autonomous agents can search, reason over structured data, and generate actionable summaries.

**Built by a PM who ships AI platforms.** This isn't a tutorial project — it reflects the kind of system design thinking I bring to building AI products at scale.

---

## What This Does

An agent that can autonomously:
1. **Search the web** for real-time information
2. **Query a local SQLite database** of financial data
3. **Synthesize findings** into structured summaries
4. **Self-evaluate** output quality, latency, and token efficiency

The agent uses Claude's native tool-use capability to decide *which* tools to invoke and *when* — no hardcoded chains.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                 Orchestrator                 │
│            (agents/orchestrator.py)          │
│                                             │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Web     │  │ Database │  │ Summary   │  │
│  │ Search  │  │ Query    │  │ Generator │  │
│  │ Tool    │  │ Tool     │  │ Tool      │  │
│  └─────────┘  └──────────┘  └───────────┘  │
└──────────────────┬──────────────────────────┘
                   │
          ┌────────▼────────┐
          │   Eval Harness  │
          │  (evals/run.py) │
          │                 │
          │  • Latency      │
          │  • Token usage  │
          │  • Quality      │
          └─────────────────┘
```

For detailed design decisions, trade-offs, and future roadmap → **[DESIGN.md](DESIGN.md)**

---

## Quick Start

### Prerequisites
- Python 3.11+
- An Anthropic API key

### Setup

```bash
# Clone
git clone https://github.com/diptirai746/ai-agent-playground.git
cd ai-agent-playground

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the agent
python main.py "What are the top 5 banks by total assets in the US?"

# Run with eval logging
python main.py "Compare JPMorgan and Bank of America's asset growth" --eval
```

---

## Project Structure

```
ai-agent-playground/
├── main.py                 # Entry point
├── agents/
│   └── orchestrator.py     # Core agent loop with tool dispatch
├── tools/
│   ├── web_search.py       # Web search tool definition
│   ├── db_query.py         # SQLite query tool
│   └── summarizer.py       # Summary generation tool
├── utils/
│   ├── logger.py           # Structured logging
│   └── config.py           # Configuration management
├── evals/
│   ├── run.py              # Evaluation harness
│   └── metrics.py          # Latency, tokens, quality scoring
├── data/
│   └── seed_db.py          # Script to populate sample SQLite DB
├── DESIGN.md               # Architecture decisions & trade-offs
├── requirements.txt
└── .env.example
```

---

## What I'd Build Next

- **Memory layer** — conversation persistence across sessions
- **Multi-agent orchestration** — specialist agents that hand off to each other
- **Streaming responses** — real-time output for better UX
- **Cost guardrails** — token budget enforcement per query
- **Retrieval tool** — RAG over a document corpus

---

## Design Philosophy

> As a PM who's built AI platforms serving millions of users, I've learned that the hardest part isn't getting an LLM to generate text — it's building the *system* around it: routing, fallbacks, evaluation, and cost control. This project is a small but complete version of that system.

See **[DESIGN.md](DESIGN.md)** for the full writeup.

---

## License

MIT

