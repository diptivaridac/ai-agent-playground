"""Database query tool — executes SQL against the local finance SQLite DB."""

import sqlite3
import json
from utils.config import Config

TOOL_DEFINITION = {
    "name": "query_database",
    "description": (
        "Query a SQLite database of US bank financial data. The database contains a "
        "'banks' table with columns: name (text), city (text), state (text), "
        "total_assets_millions (real), total_deposits_millions (real), "
        "established_year (integer), institution_type (text). "
        "Use this tool when the user asks about banks, financial institutions, "
        "assets, deposits, or comparisons between banks."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "sql": {
                "type": "string",
                "description": "A read-only SQL SELECT query to run against the database.",
            }
        },
        "required": ["sql"],
    },
}


def execute(sql: str) -> str:
    """Run a SELECT query and return results as a JSON string."""
    if not sql.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return json.dumps({"row_count": len(rows), "results": rows}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
