from selenium.webdriver.common.by import By
from Idea2.scraper.init_scraper import init_driver

def fetch_supplier_links(url):
    """
    Scrapes supplier profile links from the given URL.

    :param url: The webpage URL to scrape.
    :return: A list of supplier profile URLs.
    """
    if not url.startswith("https"):
        print("❌ Invalid URL. Please enter a valid HTTPS URL.")
        return []

    print(f"🌐 Fetching supplier links from: {url}")

    # Initialize WebDriver
    driver = init_driver(headless=True)
    driver.get(url)
    print("✅ Page loaded successfully.")

    # Extract supplier profile links
    supplier_links = []
    elements = driver.find_elements(By.CSS_SELECTOR, "a.supplier-profile")  # Modify CSS selector as needed
    print(f"🔎 Found {len(elements)} elements matching selector.")

    for elem in elements:
        href = elem.get_attribute("href")
        print(f"➡️ Found link: {href}")

        if href and href.startswith(("http", "https")):  # Fixing the `startswith` issue
            supplier_links.append(href)

    print(f"✅ Extracted {len(supplier_links)} valid supplier links.")

    driver.quit()
    return supplier_links


def test_link_scraper():
    url = input("🔗 Enter the URL to scrape supplier links from: ")

    print("\n🚀 Starting the scraping process...\n")
    links = fetch_supplier_links(url)

    print("\n📌 Extracted Links:")
    if links:
        for i, link in enumerate(links, start=1):
            print(f"{i}. {link}")
    else:
        print("⚠️ No links found. Please check the website structure or selector.")


if __name__ == "__main__":
    test_link_scraper()