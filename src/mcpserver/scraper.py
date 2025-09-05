# pricehosty.py

from playwright.async_api import async_playwright
import re

async def get_producthistory_prices(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://pricehistory.app")

        await page.fill('input[placeholder="Enter Product Link or Name"]', url)
        await page.click('button:has-text("Search")')

        await page.wait_for_timeout(3000)  # Let the page fully load

        content = await page.inner_text('body')

        prices = re.findall(r'₹[\d,]+', content)

        def clean_price(p):
            return int(p.replace('₹', '').replace(',', '').strip())

        numeric_prices = [clean_price(p) for p in prices]

        if not numeric_prices:
            await browser.close()
            return {
                "current_price": None,
                "lowest_price": None,
                "highest_price": None
            }

        # Try to extract "Current Price"
        current_price_match = re.search(r'Current Price[:\s₹]*([\d,]+)', content)
        current_price = clean_price("₹" + current_price_match.group(1)) if current_price_match else numeric_prices[0]

        lowest_price = min(numeric_prices)
        highest_price = max(numeric_prices)

        await browser.close()

        return {
            "current_price": current_price,
            "lowest_price": lowest_price,
            "highest_price": highest_price
        }
