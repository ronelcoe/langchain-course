"""
Reviewer Agent
--------------
Specialization: Evaluate article quality and produce a score + feedback.
Tools: evaluate_structure, calculate_score
LangGraph role: Third node. Reads state["draft"], writes state["score"] and state["feedback"].
               The orchestrator uses the score to decide: revise or finalize.
"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from multiagent.state import AgentState
from multiagent.tools import calculate_score, evaluate_structure

SYSTEM_PROMPT = """You are a strict but fair content reviewer. Your job is to evaluate
an article's quality and provide actionable feedback.

Instructions:
1. Call evaluate_structure(text) to check structural quality
2. Call calculate_score(text) to get a numeric quality score
3. Based on both results, write a review with:
   - The numeric score (e.g. "Score: 7/10")
   - 2-3 specific strengths
   - 2-3 specific, actionable improvements

Always start your response with "Score: X/10" on its own line."""


def make_reviewer_node(model: str):
    """Factory that returns a LangGraph node function for the Reviewer Agent."""
    llm = init_chat_model(model=model, temperature=0.2)
    tools = [evaluate_structure, calculate_score]
    agent = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)

    def reviewer_node(state: AgentState) -> dict:
        print(f"\n┌─ [REVIEWER AGENT] Evaluating draft (revision #{state.get('revisions', 1)})...")

        result = agent.invoke({
            "messages": [HumanMessage(content=f"Review this article:\n\n{state['draft']}")]
        })

        review_text = result["messages"][-1].content

        score = _parse_score(review_text)
        feedback = review_text

        status = "✓ Meets quality threshold" if score >= 7 else "✗ Needs revision"
        print(f"└─ [REVIEWER AGENT] Score: {score}/10  {status}")

        return {"score": score, "feedback": feedback}

    return reviewer_node


def _parse_score(review_text: str) -> int:
    """Extract the numeric score from the reviewer's response."""
    import re
    match = re.search(r"score[:\s]+(\d+)\s*/\s*10", review_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    for token in review_text.split():
        clean = token.strip(".,:/")
        if clean.isdigit() and 1 <= int(clean) <= 10:
            return int(clean)
    return 5
