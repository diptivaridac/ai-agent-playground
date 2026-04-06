"""Summary generator tool — produces structured summaries from collected data."""

import json

TOOL_DEFINITION = {
    "name": "generate_summary",
    "description": (
        "Generate a structured summary from data collected by other tools. "
        "Use this tool after gathering data from the database or web search "
        "to create a clear, formatted summary for the user. Useful for "
        "synthesizing multiple data points into a coherent answer."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "A short title for the summary.",
            },
            "key_findings": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of key findings or bullet points.",
            },
            "data_sources": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of data sources used (e.g., 'local database', 'web search').",
            },
        },
        "required": ["title", "key_findings"],
    },
}


def execute(title: str, key_findings: list[str], data_sources: list[str] | None = None) -> str:
    """Format findings into a structured summary."""
    summary = {
        "title": title,
        "key_findings": key_findings,
        "data_sources": data_sources or [],
        "finding_count": len(key_findings),
    }
    return json.dumps(summary, indent=2)
