import requests
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize the README Autopilot MCP
mcp = FastMCP("README Autopilot")

# CONFIGURATION
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_repo_contributors(owner: str, repo: str):
    """Fetch contributor data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def generate_contributor_grid(owner: str, repo: str, cols: int = 5):
    """
    Generates a Markdown/HTML grid of contributor avatars for a README.
    Addresses the 'TealTiger' lead for automated contributor spotlights.
    """
    contributors = get_repo_contributors(owner, repo)
    
    if isinstance(contributors, dict) and "error" in contributors:
        return contributors
        
    markdown = "### Contributors\n\n<table>\n  <tr>\n"
    
    for i, contributor in enumerate(contributors):
        login = contributor['login']
        avatar = contributor['avatar_url']
        html_url = contributor['html_url']
        
        markdown += f'    <td align="center"><a href="{html_url}"><img src="{avatar}" width="100px;" alt=""/><br /><sub><b>{login}</b></sub></a></td>\n'
        
        if (i + 1) % cols == 0:
            markdown += "  </tr>\n  <tr>\n"
            
    markdown += "  </tr>\n</table>\n"
    return markdown

@mcp.tool()
def sync_readme_metadata(owner: str, repo: str, current_readme: str):
    """
    Analyzes a README and proposes updates based on the latest repo stats 
    (stars, forks, open issues).
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    
    try:
        repo_data = requests.get(url, headers=headers).json()
        stats = f"![Stars](https://img.shields.io/github/stars/{owner}/{repo}) ![Forks](https://img.shields.io/github/forks/{owner}/{repo})"
        
        if stats not in current_readme:
            return {"action": "UPDATE", "suggested_badges": stats}
        return {"action": "NONE", "message": "Badges already present."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("README Autopilot ACTIVE. Keeping docs fresh for the A2A economy...")
    mcp.run(transport="stdio")
