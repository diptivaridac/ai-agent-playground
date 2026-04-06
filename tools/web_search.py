"""Web search tool — simulated search for demonstration purposes.

In a production system, this would call a real search API (Tavily, Brave, SerpAPI).
For this project, it returns curated results to demonstrate the tool-use pattern
without requiring a paid search API key.
"""

import json

TOOL_DEFINITION = {
    "name": "web_search",
    "description": (
        "Search the web for current information. Use this tool when the user's "
        "question requires real-time data, recent news, or information not likely "
        "to be in the local database. Returns a list of relevant search results "
        "with titles, snippets, and URLs."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up on the web.",
            }
        },
        "required": ["query"],
    },
}

# Curated results for common financial queries (demo purposes)
_MOCK_RESULTS = {
    "default": [
        {
            "title": "Federal Reserve Economic Data (FRED)",
            "snippet": "Access thousands of economic data series from the Federal Reserve Bank of St. Louis.",
            "url": "https://fred.stlouisfed.org/",
        },
        {
            "title": "FDIC BankFind Suite",
            "snippet": "Search for FDIC-insured banking institutions and access financial data.",
            "url": "https://www.fdic.gov/bankfind",
        },
    ]
}


def execute(query: str) -> str:
    """Perform a simulated web search and return results."""
    results = _MOCK_RESULTS.get("default")
    return json.dumps({
        "query": query,
        "results": results,
        "note": "These are simulated results for demonstration. In production, this would call a live search API.",
    }, indent=2)
