import requests
from app.tool.base import BaseTool, ToolResult

class WebScraperTool(BaseTool):
    name: str = "web_scraper"
    description: str = (
        "Scrapes websites for information using the Firecrawl API. "
        "The tool takes a SERP query from the provided input, "
        "calls the search API, and returns the markdown content of the result."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A SERP query",
            }
        },
        "required": ["query"],
    }

    async def execute(self, query: str, **kwargs) -> ToolResult:
        # Call the local Firecrawl search API
        try:
            response = requests.post(
                "http://localhost:3002/v1/search",
                json={
                    "query": query,
                    "limit": 1,
                    "timeout": 60000,
                    "scrapeOptions": {"formats": ["markdown"]},
                },
                headers={"Content-Type": "application/json"},
            )
        except Exception as e:
            return ToolResult(error=f"Failed to call search API: {str(e)}")

        if response.status_code != 200:
            return ToolResult(error=f"Search API returned status code {response.status_code}")

        data = response.json().get("data")
        if not data:
            return ToolResult(error="No data returned from the search API.")

        # Return the markdown content of the first result
        markdown = data[0].get("markdown")
        if not markdown:
            return ToolResult(error="No markdown content found in the search results.")

        return ToolResult(output=markdown)
