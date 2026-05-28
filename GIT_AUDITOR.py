import subprocess
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize the Git Auditor MCP
mcp = FastMCP("Git Auditor")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def audit_repository(path: str = "."):
    """
    Performs a deep audit of a Git repository to provide a 'Verified' state.
    Solves the 'Invisible Remotes' bug found in many agentic CLI tools.
    """
    if not os.path.exists(os.path.join(path, ".git")):
        return {"error": "Not a git repository."}
    
    # 1. Fetch Local Branches
    local_branches = run_command(f"cd {path} && git branch --format='%(refname:short)'").split("\n")
    
    # 2. Fetch Remote Branches (The fix for the RTK bug)
    remote_branches = run_command(f"cd {path} && git branch -r --format='%(refname:short)'").split("\n")
    
    # 3. Check for unpushed changes
    unpushed = run_command(f"cd {path} && git log @{{u}}.. --oneline")
    
    return {
        "repository_path": os.path.abspath(path),
        "branches": {
            "local": local_branches,
            "remote": remote_branches
        },
        "sync_status": {
            "is_clean": run_command(f"cd {path} && git status --porcelain") == "",
            "unpushed_commits": unpushed.split("\n") if unpushed else []
        },
        "advice": "Use 'git fetch' to ensure remote branch lists are up to date."
    }

if __name__ == "__main__":
    print("Git Auditor ACTIVE. Verifying the state of the code...")
    mcp.run(transport="stdio")
