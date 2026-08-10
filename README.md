# LangChain Agent (Claude-powered)

A single-agent LangChain project powered by Anthropic's Claude, equipped with tools for web search and live weather lookups. Built using LangChain v1.x's `create_agent` API.

## Overview

This agent uses one Claude model as its reasoning engine, with access to multiple tools it can call as needed:

- **`TavilySearch`** — a prebuilt LangChain tool for general web search
- **`get_weather_data`** — a custom tool that hits the Weatherstack API for current weather by city

The agent reads the user's request, decides (via native tool calling) which tool(s) it needs, executes them, and returns a final answer.

```
User → Agent (Claude + tools) → Answer
```

## Requirements

- Python 3.12+
- API keys for:
  - [Anthropic](https://console.anthropic.com/) (`ANTHROPIC_API_KEY`)
  - [Tavily](https://tavily.com/) (`TAVILY_API_KEY`)
  - [Weatherstack](https://weatherstack.com/) (`WEATHERSTACK_API_KEY`)

## Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -U langchain langchain-anthropic langchain-tavily python-dotenv requests
   ```

4. Create a `.env` file in the project root:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   TAVILY_API_KEY=tvly-...
   WEATHERSTACK_API_KEY=...
   ```

   > **Note:** `.env` should never be committed. Make sure it's listed in `.gitignore`.

## Usage

Run the agent:

```bash
python agent.py
```

Example query (set inside `agent.py`):

```python
response = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the current weather in Plano, Texas and how is it looking this week?"}
    ]
})
print(response["messages"][-1].content)
```

## Project Structure

```
.
├── agent.py          # Main agent script
├── .env              # API keys (not committed)
├── .gitignore
└── README.md
```

## How It Works

1. **Model** — `ChatAnthropic` (Claude Sonnet) is instantiated as the agent's reasoning engine.
2. **Tools** — Each tool is registered with a name, description, and parameter schema. Tool descriptions (docstrings) matter — they're what the model reads to decide when to use a tool.
3. **Agent** — `create_agent(model=..., tools=..., system_prompt=...)` builds a ReAct-style agent that can call tools autonomously.
4. **Invocation** — Input is a `messages` list (chat format). Output is the full message trace; the final answer is `response["messages"][-1].content`.

## Roadmap

- [ ] Add more tools (e.g., calendar, calculator, database lookups)
- [ ] Add conversation memory across turns
- [ ] Add error handling / retries for tool API calls
- [ ] Explore multi-agent orchestration (e.g., supervisor + specialist agents) as tools/scope grow

## Notes

- Uses `langchain` v1.x's `create_agent` API (not the deprecated `create_react_agent` + `AgentExecutor` pattern).
- Tool selection is handled by Claude's native tool-calling capability, not manual prompt engineering.
