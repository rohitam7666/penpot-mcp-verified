import requests
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP

# Initialize the Scientific Oracle
mcp = FastMCP("Scientific Oracle")

def query_arxiv(search_query: str, max_results: int = 3):
    """Internal helper to search ArXiv for peer-reviewed papers."""
    base_url = "http://export.arxiv.org/api/query?"
    params = f"search_query=all:{search_query}&start=0&max_results={max_results}"
    
    try:
        response = requests.get(base_url + params)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def verify_scientific_claim(claim: str):
    """
    Verifies a scientific claim by searching ArXiv for relevant papers.
    Returns the top matching abstracts and a 'Verification Context'.
    """
    raw_xml = query_arxiv(claim)
    
    if "Error" in raw_xml:
        return {"error": raw_xml}
        
    root = ET.fromstring(raw_xml)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    results = []
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text.strip()
        summary = entry.find('atom:summary', namespace).text.strip()
        link = entry.find('atom:id', namespace).text.strip()
        
        results.append({
            "title": title,
            "abstract": summary[:300] + "...",
            "source": link
        })
        
    if not results:
        return {"status": "UNVERIFIED", "message": "No peer-reviewed papers found on ArXiv for this claim."}
        
    return {
        "status": "RESEARCHED",
        "claim": claim,
        "evidence": results,
        "advice": "Agent should read the full abstracts to determine if the claim is supported or refuted."
    }

if __name__ == "__main__":
    print("Scientific Oracle ACTIVE. Grounding the agentic mind in hard science...")
    mcp.run(transport="stdio")
