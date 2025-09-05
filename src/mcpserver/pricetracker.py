# pricetracker.py

from mcp.server.fastmcp import FastMCP, Context
import asyncio
from mcpserver.scraper import get_producthistory_prices 
# Import from your other file

# Create the MCP app
mcp = FastMCP("PriceTracker")

@mcp.tool()
async def show_lowest_and_highest(url: str, ctx: Context) -> str:
    """
    Triggers Playwright to open PriceHistory.app and extract lowest, highest, and current prices.
    """
    try:
        task = asyncio.create_task(get_producthistory_prices(url))

        # Report progress while scraping
        while not task.done():
            await asyncio.sleep(1)
            await ctx.report_progress(0, 0, "Looking up price history...")

        data = await task

        cp, lp, hp = data["current_price"], data["lowest_price"], data["highest_price"]

        if cp is None and (lp is None or hp is None):
            return "❌ Couldn't extract price data. Try a different product URL."

        return (
            f"📦 **Price History** for:\n{url}\n\n"
            f"• 🔻 Lowest Price Ever: ₹{lp}\n"
            f"• 🔺 Highest Price Ever: ₹{hp}\n"
            f"• 💰 Current Price: ₹{cp}"
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Run the MCP server
if __name__ == "__main__":
    mcp.run()
