# Multi-Agent Orchestration Tutorial

A hands-on tutorial showing how **multiple specialized AI agents** collaborate
under the coordination of a **LangGraph orchestrator**.

## Architecture

```
User Request ("Write about Python")
          │
          ▼
  ┌──────────────┐
  │ Orchestrator │  ← StateGraph controls all routing
  │  (LangGraph) │
  └──────────────┘
          │
          ▼
  ┌───────────────┐     ┌───────────────┐     ┌────────────────┐
  │ Research Agent│────►│  Writer Agent │────►│ Reviewer Agent │
  │               │     │               │     │                │
  │ Tools:        │     │ Tools:        │     │ Tools:         │
  │ • search_facts│     │ • get_content │     │ • eval_struct  │
  │ • get_stats   │     │   _structure  │     │ • calc_score   │
  │ • find_exmples│     │ • get_tone    │     │                │
  └───────────────┘     └───────────────┘     └────────────────┘
                                 ▲                    │
                                 │    score < 7       │
                                 └────────────────────┘
                                       (revision loop)
```

## How It Works

### 1. Shared State
All agents communicate through a **shared state** (`AgentState`). No agent
talks directly to another — they only read/write state.

```python
class AgentState(TypedDict):
    topic: str       # Original request
    research: str    # Output from ResearchAgent
    draft: str       # Output from WriterAgent
    score: int       # Quality score from ReviewerAgent
    feedback: str    # Reviewer comments
    revisions: int   # Revision count
    final: str       # Final approved article
```

### 2. Specialized Agents
Each agent is an LLM with a focused system prompt and specific tools:

| Agent | Role | Tools |
|---|---|---|
| **ResearchAgent** | Gathers facts, stats, examples | `search_facts`, `get_statistics`, `find_examples` |
| **WriterAgent** | Drafts article from research | `get_content_structure`, `get_tone_guidelines` |
| **ReviewerAgent** | Scores and critiques the draft | `evaluate_structure`, `calculate_score` |

### 3. Orchestrator (StateGraph)
The orchestrator is a **LangGraph `StateGraph`** — a directed graph where:
- **Nodes** = agent functions
- **Edges** = data flow between agents
- **Conditional edges** = routing decisions based on state

```
START → research → writer → reviewer
                        ↑         │
                        │ (revise)│ score < 7
                        └─────────┘
                                  │ score ≥ 7
                                  ▼
                              finalize → END
```

### 4. Conditional Routing (The Orchestrator's Brain)
```python
def should_revise(state: AgentState) -> str:
    if state["score"] >= 7:
        return "finalize"      # Article approved
    if state["revisions"] >= 2:
        return "finalize"      # Max revisions hit
    return "writer"            # Send back for revision
```

## Running the Tutorial

```bash
cd langchain-course
python -m multiagent.orchestrator
```

### Expected Output
```
════════════════════════════════════════════════════════════
   MULTI-AGENT ORCHESTRATION — LangGraph Tutorial
════════════════════════════════════════════════════════════

[ORCHESTRATOR] Task received: 'Python programming language'
[ORCHESTRATOR] Pipeline: Research → Write → Review → (Revise?) → Done

┌─ [RESEARCH AGENT] Starting...
│  Topic: 'Python programming language'
└─ [RESEARCH AGENT] Done ✓  (189 words collected)

┌─ [WRITER AGENT] Writing FIRST DRAFT...
└─ [WRITER AGENT] Done ✓  (312 words drafted)

┌─ [REVIEWER AGENT] Evaluating draft (revision #1)...
└─ [REVIEWER AGENT] Score: 6/10  ✗ Needs revision

[ORCHESTRATOR] Score 6/10 < 7 → Sending back for revision

┌─ [WRITER AGENT] Writing REVISION...
│  Addressing feedback from reviewer (revision #1)
└─ [WRITER AGENT] Done ✓  (387 words drafted)

┌─ [REVIEWER AGENT] Evaluating draft (revision #2)...
└─ [REVIEWER AGENT] Score: 8/10  ✓ Meets quality threshold

[ORCHESTRATOR] Score 8/10 ≥ 7 → Approving draft

════════════════════════════════════════════════════════════
   FINAL OUTPUT
════════════════════════════════════════════════════════════
...article content...

[DONE] Completed in 2 revision(s). Final score: 8/10
```

## Key Concepts Demonstrated

| Concept | Where to See It |
|---|---|
| Agent specialization | `agents/research_agent.py`, `agents/writer_agent.py`, etc. |
| Shared state | `state.py` → `AgentState` TypedDict |
| Graph construction | `orchestrator.py` → `build_graph()` |
| Conditional routing | `orchestrator.py` → `should_revise()` |
| Revision loop | Graph edge: `reviewer → writer → reviewer` |
| Dummy tools | `tools.py` → simulates real APIs |

## Configuration

In `orchestrator.py`:

```python
MODEL = "gpt-4o-mini"          # or "ollama:qwen2.5:1.5b" for local
QUALITY_THRESHOLD = 7           # Reviewer score to approve (1-10)
MAX_REVISIONS = 2               # Max revision loops
```

## Installation

```bash
pip install langgraph langchain langchain-openai python-dotenv
```

Add your API key to `.env`:
```
OPENAI_API_KEY=sk-...
```
