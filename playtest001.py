from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=False)
    page = browser.new_page()
    page.goto("http://playwright.dev")
    print(page.title())
    browser.close()