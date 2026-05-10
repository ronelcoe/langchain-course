from typing import TypedDict


class AgentState(TypedDict):
    topic: str          # Original user request
    research: str       # Output from ResearchAgent
    draft: str          # Output from WriterAgent
    score: int          # Quality score from ReviewerAgent (1-10)
    feedback: str       # Reviewer feedback text
    revisions: int      # How many revision cycles have happened
    final: str          # Final approved article
