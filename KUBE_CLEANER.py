import re
import yaml
from mcp.server.fastmcp import FastMCP

# Initialize the KubeAgent Cleaner MCP
mcp = FastMCP("KubeAgent Cleaner")

@mcp.tool()
def audit_kubernetes_yaml(yaml_content: str, unused_fields: list):
    """
    Scans Kubernetes YAML configurations for specific unused or ghost fields.
    Helps agents maintain clean, production-ready infrastructure.
    """
    try:
        data = yaml.safe_load(yaml_content)
        found_issues = []
        
        # Simple recursive check for unused fields
        def check_unused(obj, fields):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in fields:
                        found_issues.append({
                            "field": k,
                            "message": f"Unused field '{k}' detected in configuration.",
                            "severity": "CLEANUP"
                        })
                    check_unused(v, fields)
            elif isinstance(obj, list):
                for item in obj:
                    check_unused(item, fields)

        check_unused(data, unused_fields)
        
        if not found_issues:
            return {"status": "CLEAN", "message": "No unused fields detected."}
            
        return {
            "status": "DIRTY",
            "issues": found_issues,
            "advice": "Remove these fields to simplify the CRD and reduce configuration bloat."
        }
    except Exception as e:
        return {"error": f"Invalid YAML: {str(e)}"}

if __name__ == "__main__":
    print("KubeAgent Cleaner ACTIVE. Scrubbing the infrastructure...")
    mcp.run(transport="stdio")
