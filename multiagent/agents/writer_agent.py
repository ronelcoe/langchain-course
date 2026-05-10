"""
Writer Agent
------------
Specialization: Draft a well-structured article from research notes.
Tools: get_content_structure, get_tone_guidelines
LangGraph role: Second node. Reads state["research"], writes state["draft"].
               On revision cycles it also reads state["feedback"].
"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from multiagent.state import AgentState
from multiagent.tools import get_content_structure, get_tone_guidelines

SYSTEM_PROMPT = """You are a professional content writer. Your job is to write a clear,
engaging article based on research notes provided to you.

Instructions:
1. Call get_content_structure("article") to get the structural template
2. Call get_tone_guidelines("educational") for tone guidance
3. Write the full article following the structure and tone guidelines
4. If reviewer feedback is provided, address every point in the feedback

Return ONLY the article text. No meta-commentary."""


def make_writer_node(model: str):
    """Factory that returns a LangGraph node function for the Writer Agent."""
    llm = init_chat_model(model=model, temperature=0.7)
    tools = [get_content_structure, get_tone_guidelines]
    agent = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)

    def writer_node(state: AgentState) -> dict:
        is_revision = state.get("revisions", 0) > 0
        label = "REVISION" if is_revision else "FIRST DRAFT"
        print(f"\n┌─ [WRITER AGENT] Writing {label}...")

        prompt_parts = [
            f"Topic: {state['topic']}",
            f"\nResearch Notes:\n{state['research']}",
        ]
        if is_revision and state.get("feedback"):
            prompt_parts.append(f"\nReviewer Feedback to Address:\n{state['feedback']}")
            print(f"│  Addressing feedback from reviewer (revision #{state['revisions']})")

        result = agent.invoke({
            "messages": [HumanMessage(content="\n".join(prompt_parts))]
        })

        draft = result["messages"][-1].content
        print(f"└─ [WRITER AGENT] Done ✓  ({len(draft.split())} words drafted)")
        return {
            "draft": draft,
            "revisions": state.get("revisions", 0) + 1,
        }

    return writer_node
