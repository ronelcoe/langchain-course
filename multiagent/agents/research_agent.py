"""
Research Agent
--------------
Specialization: Gather facts, statistics, and examples about a topic.
Tools: search_facts, get_statistics, find_examples
LangGraph role: First node in the pipeline. Populates state["research"].
"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from multiagent.state import AgentState
from multiagent.tools import find_examples, get_statistics, search_facts

SYSTEM_PROMPT = """You are a research specialist. Your job is to gather comprehensive
information about the given topic using your available tools.

Follow this exact sequence:
1. Call search_facts to get key facts
2. Call get_statistics to get relevant numbers and data
3. Call find_examples to get real-world use cases
4. Compile everything into a clear, structured research summary

Return ONLY the research summary. Do not add extra commentary."""


def make_research_node(model: str):
    """Factory that returns a LangGraph node function for the Research Agent."""
    llm = init_chat_model(model=model, temperature=0.2)
    tools = [search_facts, get_statistics, find_examples]
    agent = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)

    def research_node(state: AgentState) -> dict:
        print("\n┌─ [RESEARCH AGENT] Starting...")
        print(f"│  Topic: '{state['topic']}'")

        result = agent.invoke({
            "messages": [HumanMessage(content=f"Research this topic thoroughly: {state['topic']}")]
        })

        research = result["messages"][-1].content
        print(f"└─ [RESEARCH AGENT] Done ✓  ({len(research.split())} words collected)")
        return {"research": research}

    return research_node
