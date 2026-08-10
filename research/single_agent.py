# -----------------------------------------------------------------------
# Clean, working setup for a Claude-powered LangChain agent with tools
# Install first (run once in terminal or a notebook cell with !):
#
#   pip install -U langchain langchain-anthropic langchain-tavily python-dotenv requests
#
# Your .env file (same folder as this notebook/script) should contain:
#   ANTHROPIC_API_KEY=sk-ant-...
#   TAVILY_API_KEY=tvly-...
#   WEATHERSTACK_API_KEY=...
# -----------------------------------------------------------------------

import os
import requests
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# Sanity check keys loaded (prints True/False, never the actual secret)
print("Keys loaded:", bool(ANTHROPIC_API_KEY), bool(TAVILY_API_KEY), bool(WEATHERSTACK_API_KEY))

# -----------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

model = ChatAnthropic(model="claude-sonnet-4-5")

# -----------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------
from langchain_tavily import TavilySearch
from langchain.tools import tool

search_tool = TavilySearch(max_results=2)

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """
    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)
    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

tools = [search_tool, get_weather_data]

# -----------------------------------------------------------------------
# Agent
# -----------------------------------------------------------------------
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=(
        "You are a helpful assistant. Use the search tool to look up facts "
        "and the weather tool to get current weather when needed."
    ),
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content":  "what is the current weather in Plano, Texas and how is it looking this week ?",
        }
    ]
})

# The final answer is the last message in the returned messages list
print(response["messages"][-1].content)