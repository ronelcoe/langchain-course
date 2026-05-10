"""
Multi-Agent Orchestrator
========================
Uses LangGraph StateGraph to wire specialized agents into a pipeline.

Flow:
                    ┌─────────────────────────────────────────┐
                    │                                         │
  START ──► research ──► writer ──► reviewer ──► (score≥7?) ──► END
                              ▲          │
                              │  score<7 │ (max 2 revisions)
                              └──────────┘

Each node is a specialized AI agent. The orchestrator (StateGraph) controls
routing — agents never talk to each other directly.
"""

import os
from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

load_dotenv()
# Support both OPEN_API_KEY and OPENAI_API_KEY env var names
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPEN_API_KEY", "")

from multiagent.agents.research_agent import make_research_node
from multiagent.agents.reviewer_agent import make_reviewer_node
from multiagent.agents.writer_agent import make_writer_node
from multiagent.state import AgentState

# ── Configuration ──────────────────────────────────────────────────────────────

MODEL = "gpt-4o-mini"          # Switch to "ollama:qwen2.5:1.5b" for local
QUALITY_THRESHOLD = 7           # Reviewer score needed to approve the draft
MAX_REVISIONS = 2               # Maximum writer revision cycles allowed


# ── Router ─────────────────────────────────────────────────────────────────────

def should_revise(state: AgentState) -> str:
    """
    The orchestrator's decision logic after reviewing a draft.
    Returns the name of the next node to run.
    """
    score = state.get("score", 0)
    revisions = state.get("revisions", 0)

    if score >= QUALITY_THRESHOLD:
        print(f"\n[ORCHESTRATOR] Score {score}/10 ≥ {QUALITY_THRESHOLD} → Approving draft")
        return "finalize"

    if revisions >= MAX_REVISIONS:
        print(f"\n[ORCHESTRATOR] Max revisions ({MAX_REVISIONS}) reached → Finalizing as-is")
        return "finalize"

    print(f"\n[ORCHESTRATOR] Score {score}/10 < {QUALITY_THRESHOLD} → Sending back for revision")
    return "writer"


def finalize_node(state: AgentState) -> dict:
    """Marks the best draft as the final output."""
    return {"final": state["draft"]}


# ── Graph Construction ─────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    research_node = make_research_node(MODEL)
    writer_node = make_writer_node(MODEL)
    reviewer_node = make_reviewer_node(MODEL)

    graph = StateGraph(AgentState)

    graph.add_node("research", research_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("finalize", finalize_node)

    graph.add_edge(START, "research")
    graph.add_edge("research", "writer")
    graph.add_edge("writer", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "writer": "writer",
            "finalize": "finalize",
        },
    )

    graph.add_edge("finalize", END)

    return graph.compile()


# ── Entry Point ────────────────────────────────────────────────────────────────

def run(topic: str) -> str:
    print("\n" + "═" * 60)
    print("   MULTI-AGENT ORCHESTRATION — LangGraph Tutorial")
    print("═" * 60)
    print(f"\n[ORCHESTRATOR] Task received: '{topic}'")
    print("[ORCHESTRATOR] Pipeline: Research → Write → Review → (Revise?) → Done\n")

    app = build_graph()

    initial_state: AgentState = {
        "topic": topic,
        "research": "",
        "draft": "",
        "score": 0,
        "feedback": "",
        "revisions": 0,
        "final": "",
    }

    final_state = app.invoke(initial_state)

    print("\n" + "═" * 60)
    print("   FINAL OUTPUT")
    print("═" * 60)
    print(final_state["final"])
    print("\n" + "═" * 60)
    print(f"[DONE] Completed in {final_state['revisions']} revision(s). "
          f"Final score: {final_state['score']}/10")

    return final_state["final"]


if __name__ == "__main__":
    run("Python programming language")
