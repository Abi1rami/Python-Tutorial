from playwright.async_api import async_playwright
import asyncio

async def get_match_score_news():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Opening Google...")
        await page.goto("https://www.google.com")
        await page.wait_for_timeout(2000)

        # Search for match score
        print("Searching for match score...")
        await page.fill('textarea[name="q"]', "latest cricket match score 2026")
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click News tab
        print("Clicking News tab...")
        await page.click('text=News')
        await page.wait_for_timeout(3000)

        # Get all news headlines
        print("Getting latest news...")
        articles = await page.query_selector_all('article')
        
        print("\n===== LATEST MATCH SCORE NEWS =====")
        count = 1
        for article in articles[:10]:
            text = await article.inner_text()
            if text.strip():
                print(f"{count}. {text.strip()[:100]}")
                count += 1

        # Click first news link safely
        print("\nClicking first news link...")
        try:
            # Try clicking first article link
            first_link = await page.query_selector('article a')
            if first_link:
                await first_link.click()
                await page.wait_for_timeout(3000)
            else:
                # Get all links and click first news one
                links = await page.query_selector_all('a[href*="http"]')
                for link in links:
                    href = await link.get_attribute('href')
                    if href and 'google' not in href:
                        await link.click()
                        break
        except Exception as e:
            print(f"Could not click link: {e}")

        await page.wait_for_timeout(3000)
        print("Current URL:", page.url)
        print("Done!")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_match_score_news())
    