import requests
import os
from mcp.server.fastmcp import FastMCP

# Initialize the GitLab Sentinel MCP
mcp = FastMCP("GitLab Sentinel")

# CONFIGURATION
GITLAB_API_URL = os.environ.get("GITLAB_API_URL", "https://gitlab.com/api/v4")
GITLAB_ACCESS_TOKEN = os.environ.get("GITLAB_ACCESS_TOKEN", "")

def call_gitlab_api(endpoint, method="GET", data=None):
    if not GITLAB_ACCESS_TOKEN:
        return {"error": "Missing GITLAB_ACCESS_TOKEN."}
    
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}
    
    try:
        if method == "POST":
            response = requests.post(f"{POLAR_API_URL}/{endpoint}", headers=headers, json=data)
        else:
            response = requests.get(f"{GITLAB_API_URL}/{endpoint}", headers=headers)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def find_high_priority_bugs(project_id: str):
    """
    Scans a GitLab project for issues labeled 'bug' or 'critical'.
    Agents use this to prioritize their workload.
    """
    return call_gitlab_api(f"projects/{project_id}/issues?labels=bug,critical&state=opened")

@mcp.tool()
def submit_merge_request(project_id: str, source_branch: str, target_branch: str, title: str):
    """
    Automatically creates a Merge Request (MR) in GitLab.
    This is how the agent 'delivers' its work for payment.
    """
    data = {
        "id": project_id,
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
        "remove_source_branch": True
    }
    return call_gitlab_api(f"projects/{project_id}/merge_requests", method="POST", data=data)

if __name__ == "__main__":
    print("GitLab Sentinel ACTIVE. Securing the enterprise pipeline...")
    mcp.run(transport="stdio")
