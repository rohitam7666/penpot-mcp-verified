import re
from mcp.server.fastmcp import FastMCP

# Initialize the Security Sentinel
mcp = FastMCP("Security Sentinel")

# DATA: Known "Evil" Patterns (Simplified for the Hackathon)
EVIL_PATTERNS = [
    {
        "id": "UNAUTHORIZED_SUDO",
        "pattern": r"sudo\s+.*NOPASSWD",
        "message": "Potential privilege escalation detected (NOPASSWD in sudoers).",
        "severity": "CRITICAL"
    },
    {
        "id": "LOG_WIPING",
        "pattern": r"rm\s+.*\.log|cat\s+/dev/null\s+>.*",
        "message": "Attempt to wipe logs detected. This is a common sign of a breach.",
        "severity": "HIGH"
    },
    {
        "id": "HIDDEN_EXEC",
        "pattern": r"chmod\s+\+x\s+\..*",
        "message": "Attempt to make a hidden file executable.",
        "severity": "WARNING"
    }
]

@mcp.tool()
def audit_system_logs(log_text: str):
    """
    Analyzes system logs or command history for 'Evil' patterns.
    Designed for autonomous security incident response.
    """
    findings = []
    
    for pattern in EVIL_PATTERNS:
        matches = re.finditer(pattern["pattern"], log_text, re.IGNORECASE)
        for match in matches:
            findings.append({
                "type": pattern["id"],
                "message": pattern["message"],
                "severity": pattern["severity"],
                "evidence": match.group(0)
            })
            
    if not findings:
        return {"status": "SECURE", "message": "No obvious signs of 'Evil' detected."}
    
    return {
        "status": "ALERT",
        "findings": findings,
        "recommendation": "Quarantine the affected environment and rotate all keys."
    }

if __name__ == "__main__":
    print("Security Sentinel ACTIVE. Hunting for 'Evil' in the logs...")
    mcp.run(transport="stdio")
