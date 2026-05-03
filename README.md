# langchain-course

Small LangChain experiments: chat models, tooling, and a **ReAct-style** agent loop (LLM chooses tools, observes results, repeats until an answer).

## Agent (ReAct-style) implementation

The manual reasoning + tool loop lives in **`[agent-loop-toll.py](./agent-loop-toll.py)`**. It mirrors the **ReAct** idea (thought → tool call → observation → repeat), without using LangChain’s higher-level agent executor—you can compare it with the docs below.

**Further reading**

- [LangChain — Agents overview](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph — Quickstart / ReAct-style agents](https://docs.langchain.com/oss/python/langgraph/quickstart)

## Requirements

- Python **3.12+**
- Dependencies: **`uv sync`** (see `pyproject.toml`) or **`pip install -r requirements.txt`**
- Local model: **[Ollama](https://ollama.com/)** with the model tag used in the script (e.g. `qwen3.5:2b`)
- Optional: LangSmith / tracing env vars if you use `@traceable` in that script

## Run

```bash
cd langchain-course
uv run python agent-loop-toll.py
```

## Sample run

```text
Starting agent loop toll...
Running agent loop for question: What is the price of a discounted apple?

============================================================

 --- Iteration 1 ---
  [Tool Selected] get_product_description with args: {'product': 'apple'}
Getting description for product: (apple')
  [Tool Result] A red apple

 --- Iteration 2 ---
  [Tool Selected] get_product_price with args: {'product': 'apple'}
Getting price for product: (apple')
  [Tool Result] 10.0

 --- Iteration 3 ---
  [Tool Selected] get_product_price with args: {'product': 'apple'}
Getting price for product: (apple')
  [Tool Result] 10.0

 --- Iteration 4 ---
  [Tool Selected] get_product_price with args: {'product': 'apple'}
Getting price for product: (apple')
  [Tool Result] 10.0

 --- Iteration 5 ---
  [Tool Selected] get_product_price with args: {'product': 'apple'}
Getting price for product: (apple')
  [Tool Result] 10.0

 --- Iteration 6 ---
  [Tool Selected] get_product_discount with args: {'product': 'apple'}
Getting discount for product: (apple')
  [Tool Result] 0.1

 --- Iteration 7 ---

 Final answer: The price of a discounted apple is 9.9.

Here's the breakdown:
- Regular price: 10.0
- Discount: 0.1
- Discounted price: 9.9
Agent loop toll completed.
```

*(Output depends on model and prompts; truncation or different tool choices are normal.)*
