from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.tool import tool_call
from langsmith import traceable

load_dotenv()
MAX_ITERATIONS = 10
MODEL = "ollama:qwen3.5:2b"

@tool
def get_product_price(product: str) -> float:
    """Get the price of a product in the catalog"""
    print(f"Getting price for product: ({product}')")
    prices = {
        "apple": 10.0,
        "banana": 20.0,
        "cherry": 30.0,
    }
    return prices.get(product, 0.0)

@tool
def get_product_description(product: str) -> str:
    """Get the description of a product"""
    print(f"Getting description for product: ({product}')")
    descriptions = {
        "apple": "A red apple",
        "banana": "A yellow banana",
        "cherry": "A red cherry",
    }
    return descriptions.get(product, "No description available")

@tool
def get_product_availability(product: str) -> bool:
    """Get the availability of a product"""
    print(f"Getting availability for product: ({product}')")
    availability = {
        "apple": True,
        "banana": False,
        "cherry": True,
    }
    return availability.get(product, False)

@tool
def get_product_discount(product: str) -> float:
    """Get the discount of a product"""
    print(f"Getting discount for product: ({product}')")
    discounts = {
        "apple": 0.1,
        "banana": 0.2,
        "cherry": 0.3,
    }
    return discounts.get(product, 0.0)

def main():
    llm = init_chat_model(model=MODEL, temperature=0.0)
    messages = [
        SystemMessage(content="You are a helpful assistant that can answer questions about the product catalog."),
        HumanMessage(content="What is the price of an apple?"),
    ]
    response = llm.invoke(messages)
    print(response.content)

@traceable(name="agent_loop_toll")
def run_agent_loop(question: str):
    tools = [get_product_price, get_product_description, get_product_availability, get_product_discount]
    tools_dict = {tool.name: tool for tool in tools}

    llm = init_chat_model(model=MODEL, temperature=0.0)
    llm_with_tools = llm.bind_tools(tools)

    print(f"Running agent loop for question: ({question}')")
    print("=" * 60)

    messages = [
        SystemMessage(
            content=(
                "You are a helful shopping assistant "
                "You have access to a product catalog tool and a discount tool. \n\n"
                "STRICT RULES - you must follow these exactly:\n"
                "1. NEVER guess or assime any product price. "
                "2. Only call apply_discount AFTER you have received a price from get_product_price.\n"
                "3. Make sure the product is available in the stock otherwise inform the user that it is out of stock."
            )
        ),
        HumanMessage(content=question)
    ]

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n --- Iteration {iteration} ---")
        ai_message = llm_with_tools.invoke(messages)
        tool_calls = ai_message.tool_calls

        if not tool_calls:
            print(f"\n Final answer: {ai_message.content}")
            return ai_message.content

         # If no tool calls, this is the final answer
        if not tool_calls:
            print(f"\nFinal Answer: {ai_message.content}")
            return ai_message.content

        # Process only the FIRST tool call — force one tool per iteration
        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")

        print(f"  [Tool Selected] {tool_name} with args: {tool_args}")

        tool_to_use = tools_dict.get(tool_name)
        if tool_to_use is None:
            raise ValueError(f"Tool '{tool_name}' not found")

        observation = tool_to_use.invoke(tool_args)

        print(f"  [Tool Result] {observation}")

        messages.append(ai_message)
        messages.append(
            ToolMessage(content=str(observation), tool_call_id=tool_call_id)
        )

    print("ERROR: Max iterations reached without a final answer")
    return None


if __name__ == "__main__":
    print("Starting agent loop toll...")
    run_agent_loop("What is the price of a discounted banana?")
    print("Agent loop toll completed.")