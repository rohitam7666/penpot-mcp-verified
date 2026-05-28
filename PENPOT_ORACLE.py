import re
import json
from mcp.server.fastmcp import FastMCP

# Initialize the Penpot Quality Oracle
mcp = FastMCP("Penpot Quality Oracle")

# DATA: Known API "Gotchas" and Anti-Patterns
GOTCHAS = [
    {
        "id": "RACE_CONDITION_PAGE_WRITE",
        "pattern": r"page\.switch.*(file\.write|createShape)",
        "message": "Page switch and write detected in same snippet. This often causes race conditions in Penpot.",
        "severity": "CRITICAL"
    },
    {
        "id": "DEPRECATED_APPEND",
        "pattern": r"\.appendChild\(",
        "message": "Using deprecated .appendChild(). Use .insertAt() for better layer order control.",
        "severity": "WARNING"
    },
    {
        "id": "UNSAFE_TRANSFORM",
        "pattern": r"\.setTransform\(.*\[.*\].*\)",
        "message": "Raw matrix transform detected without coordinate verification.",
        "severity": "WARNING"
    }
]

@mcp.tool()
def validate_penpot_script(js_code: str):
    """
    Analyzes a Penpot Plugin JavaScript snippet for known bugs and anti-patterns.
    Agents should call this BEFORE executing code to ensure reliability.
    """
    issues = []
    
    for gotcha in GOTCHAS:
        if re.search(gotcha["pattern"], js_code, re.IGNORECASE | re.DOTALL):
            issues.append({
                "type": gotcha["id"],
                "message": gotcha["message"],
                "severity": gotcha["severity"]
            })
            
    if not issues:
        return {"status": "PASS", "message": "Code follows best practices."}
    
    return {
        "status": "FAIL",
        "issues": issues,
        "advice": "Modify your code to resolve CRITICAL errors before attempting to run in Penpot."
    }

@mcp.tool()
def get_best_practices():
    """Retrieve the current knowledge base of Penpot A2A design standards."""
    return GOTCHAS

if __name__ == "__main__":
    print("Penpot Quality Oracle ACTIVE. Protecting the A2A Design Economy...")
    mcp.run(transport="stdio")
