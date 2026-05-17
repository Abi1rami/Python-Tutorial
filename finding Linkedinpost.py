from playwright.async_api import async_playwright
import asyncio

async def linkedin_bulk_hiring():
    async with async_playwright() as p:

        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # ============================================
        # STEP 1 - Open Bing
        # ============================================
        print("Opening Bing...")
        await page.goto("https://www.bing.com")
        await page.wait_for_timeout(5000)

        # ============================================
        # STEP 2 - Search LinkedIn Bulk Hiring
        # ============================================
        print("Searching Bulk Hiring posts...")
        try:
            # Bing search box selector
            await page.click('#sb_form_q')
            await page.wait_for_timeout(1000)
            await page.fill('#sb_form_q',
                           'site:linkedin.com "Bulk Hiring"')
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)
            print("✅ Search completed!")

        except Exception as e:
            print(f"Trying alternate selector... {e}")
            try:
                await page.click('input[id="sb_form_q"]')
                await page.type('input[id="sb_form_q"]',
                               'site:linkedin.com "Bulk Hiring"')
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)
            except Exception as e2:
                print(f"Search error: {e2}")

        # ============================================
        # STEP 3 - Fetch All Results
        # ============================================
        print("\nFetching posts...")
        found_posts = []

        # Scroll to load more
        for i in range(3):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            print(f"Scrolling... {i+1}/3")

        # Get all results
        results = await page.query_selector_all('li.b_algo')
        print(f"Total results found: {len(results)}")

        # ============================================
        # STEP 4 - Filter LinkedIn Posts
        # ============================================
        print("\n===== BULK HIRING LINKEDIN POSTS =====\n")

        for result in results:
            try:
                # Get title
                title_el = await result.query_selector('h2')
                title    = await title_el.inner_text() if title_el else "No Title"

                # Get link
                link_el  = await result.query_selector('a')
                link     = await link_el.get_attribute('href') if link_el else "No URL"

                # Get description
                desc_el  = await result.query_selector('p')
                desc     = await desc_el.inner_text() if desc_el else ""

                # Filter LinkedIn posts
                if link and 'linkedin.com' in link:
                    print(f"✅ Title : {title.strip()}")
                    print(f"   URL   : {link}")
                    print(f"   Desc  : {desc.strip()[:150]}")
                    print("-" * 60)

                    found_posts.append({
                        "title": title.strip(),
                        "url"  : link,
                        "desc" : desc.strip()
                    })

            except Exception as e:
                pass

        # ============================================
        # STEP 5 - Click First Post
        # ============================================
        if found_posts:
            print(f"\nOpening first post: {found_posts[0]['title']}")
            await page.goto(found_posts[0]['url'])
            await page.wait_for_timeout(5000)
            print(f"✅ Opened: {page.url}")
        else:
            print("❌ No Bulk Hiring posts found!")

        # ============================================
        # STEP 6 - Summary
        # ============================================
        print("\n===== SUMMARY =====")
        print(f"✅ Total posts found: {len(found_posts)}")
        for i, post in enumerate(found_posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   {post['url']}")

        await page.wait_for_timeout(3000)
        await browser.close()
        print("\nBrowser closed!")

if __name__ == "__main__":
    asyncio.run(linkedin_bulk_hiring())