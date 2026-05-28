import requests
import os
from mcp.server.fastmcp import FastMCP

# Initialize the Twenty CRM Bridge MCP
mcp = FastMCP("Twenty CRM Bridge")

# CONFIGURATION
TWENTY_API_URL = os.environ.get("TWENTY_API_URL", "https://api.twenty.com/rest")
TWENTY_ACCESS_TOKEN = os.environ.get("TWENTY_ACCESS_TOKEN", "")

def call_twenty_api(endpoint, method="GET", data=None):
    if not TWENTY_ACCESS_TOKEN:
        return {"error": "Missing TWENTY_ACCESS_TOKEN."}
    
    headers = {
        "Authorization": f"Bearer {TWENTY_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{TWENTY_API_URL}/{endpoint}"
        if method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_crm_contacts(query: str):
    """
    Search for contacts in Twenty CRM using a simplified natural language query.
    Agents use this to find customer records without complex SQL.
    """
    return call_twenty_api(f"contacts?filter[name][contains]={query}")

@mcp.tool()
def update_deal_status(deal_id: str, stage: str):
    """
    Updates the stage of a deal in the sales pipeline.
    Includes a 'Verification Loop' to ensure the pipeline state is updated.
    """
    # 1. Update the deal
    result = call_twenty_api(f"opportunities/{deal_id}", method="PATCH", data={"stage": stage})
    
    if "error" in result:
        return result
        
    # 2. VERIFICATION LOOP
    verification = call_twenty_api(f"opportunities/{deal_id}")
    if verification.get("stage") == stage:
        return {"status": "SUCCESS", "message": f"Deal {deal_id} moved to {stage}."}
    
    return {"status": "STALE", "message": "API confirmed update but state has not persisted yet."}

if __name__ == "__main__":
    print("Twenty CRM Bridge ACTIVE. Automating the sales pipeline...")
    mcp.run(transport="stdio")
