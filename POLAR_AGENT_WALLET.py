import requests
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize the Polar Agent Wallet MCP
mcp = FastMCP("Polar Agent Wallet")

# CONFIGURATION
POLAR_API_URL = os.environ.get("POLAR_API_URL", "https://api.polar.sh/v1")
POLAR_ACCESS_TOKEN = os.environ.get("POLAR_ACCESS_TOKEN", "")

def call_polar_api(endpoint, method="GET", data=None):
    if not POLAR_ACCESS_TOKEN:
        return {"error": "Missing POLAR_ACCESS_TOKEN."}
    
    headers = {
        "Authorization": f"Bearer {POLAR_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "POST":
            response = requests.post(f"{POLAR_API_URL}/{endpoint}", headers=headers, json=data)
        else:
            response = requests.get(f"{POLAR_API_URL}/{endpoint}", headers=headers)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def check_agent_balance(customer_id: str):
    """
    Retrieves the real-time credit balance for an agent.
    Agents use this to know if they have enough 'gas' to complete a task.
    """
    # Using the Polar Customer State/Meters API
    return call_polar_api(f"customers/{customer_id}/state")

@mcp.tool()
def log_agent_task(customer_id: str, task_name: str, units: int = 1):
    """
    Logs a completed task to Polar for usage-based billing.
    """
    event_data = {
        "name": "agent_task_completed",
        "customer_id": customer_id,
        "properties": {
            "task": task_name,
            "units": units
        }
    }
    return call_polar_api("events", method="POST", data=event_data)

@mcp.tool()
def get_refill_url(product_id: str):
    """
    Generates a checkout link for the user to buy more agent credits.
    """
    # Logic to return a Polar Checkout URL
    return {
        "topup_url": f"https://polar.sh/checkout/{product_id}",
        "message": "Please use this link to add credits to your agent's wallet."
    }

if __name__ == "__main__":
    print("Polar Agent Wallet ACTIVE. Powering the autonomous economy...")
    mcp.run(transport="stdio")
