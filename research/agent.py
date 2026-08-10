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

model = ChatAnthropic(model="claude-sonnet-4-5")

# -----------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------
from langchain_tavily import TavilySearch
from langchain.tools import tool
import requests

search_tool = TavilySearch(max_results=2)


prompt = model.invoke("what is the capital of France?")

print(prompt)