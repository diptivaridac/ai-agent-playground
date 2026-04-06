"""Core agent orchestrator — drives the tool-use loop with Claude."""

import time
import anthropic

from utils.config import Config
from utils.logger import RunLog
from tools import db_query, web_search, summarizer

# Registry: maps tool names to their execute functions
TOOL_REGISTRY = {
    "query_database": db_query.execute,
    "web_search": web_search.execute,
    "generate_summary": summarizer.execute,
}

# Tool definitions sent to Claude
TOOL_DEFINITIONS = [
    db_query.TOOL_DEFINITION,
    web_search.TOOL_DEFINITION,
    summarizer.TOOL_DEFINITION,
]

SYSTEM_PROMPT = """You are a helpful research agent with access to tools. Your job is to 
answer the user's question by using the right tools in the right order.

Guidelines:
- Use the database tool for structured queries about US banks.
- Use the web search tool for real-time or external information.
- Use the summary tool to synthesize findings when you have enough data.
- Be concise and cite your data sources.
- If the database doesn't have what you need, say so — don't hallucinate data."""


class Orchestrator:
    """Runs the agent loop: send query → handle tool calls → return result."""

    def __init__(self):
        Config.validate()
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.run_log = RunLog()

    def run(self, query: str, eval_mode: bool = False) -> str:
        """Execute a query through the agent loop. Returns the final text response."""
        self.run_log = RunLog(query=query, start_time=time.time())

        messages = [{"role": "user", "content": query}]

        for round_num in range(1, Config.MAX_TOOL_ROUNDS + 1):
            self.run_log.rounds = round_num

            response = self.client.messages.create(
                model=Config.MODEL,
                max_tokens=Config.MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            # Track token usage
            self.run_log.input_tokens += response.usage.input_tokens
            self.run_log.output_tokens += response.usage.output_tokens

            # Check if we're done (no more tool calls)
            if response.stop_reason == "end_turn":
                self.run_log.end_time = time.time()
                if eval_mode:
                    self.run_log.print_summary()
                return self._extract_text(response)

            # Process tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    self.run_log.log_tool_call(block.name, block.input, result)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # Append assistant response and tool results to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        # If we exhausted all rounds
        self.run_log.end_time = time.time()
        if eval_mode:
            self.run_log.print_summary()
        return "Agent reached maximum tool rounds without a final answer."

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Dispatch a tool call to the appropriate handler."""
        handler = TOOL_REGISTRY.get(tool_name)
        if not handler:
            return f"Error: Unknown tool '{tool_name}'"
        try:
            return handler(**tool_input)
        except Exception as e:
            return f"Error executing {tool_name}: {e}"

    def _extract_text(self, response) -> str:
        """Pull text blocks from the API response."""
        return "\n".join(
            block.text for block in response.content if hasattr(block, "text")
        )
