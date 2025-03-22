from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseScraper import BaseScraper
import time
import json
import os


class IndiaMARTScraper(BaseScraper):
    """Scraper for extracting supplier data from IndiaMART."""

    BASE_URL = "https://dir.indiamart.com/search.mp?ss={query}"
    MIN_SUPPLIERS = 300  # Minimum suppliers to extract before stopping
    SCROLL_LIMIT = 3  # Maximum number of scroll attempts

    def __init__(self, search_queries=None, custom_urls=None):
        super().__init__()
        self.search_queries = search_queries or []
        self.custom_urls = custom_urls or []
        self.all_suppliers = []

    def run_scraper(self):
        """Runs the scraper for multiple product searches or URLs."""
        urls_to_scrape = self.custom_urls if self.custom_urls else [
            self.BASE_URL.format(query=query.replace(" ", "+")) for query in self.search_queries
        ]

        for idx, url in enumerate(urls_to_scrape):
            query = self.search_queries[idx] if self.search_queries else f"Custom URL {idx+1}"
            print(f"\n🔍 Searching: {query}")
            print(f"🌐 URL: {url}")

            self.fetch_page(url)
            supplier_data = self.parse_page(query)
            print(f"📦 Extracted {len(supplier_data)} suppliers for {query}")
            self.all_suppliers.extend(supplier_data)

        self.save_data(self.all_suppliers, "indiamart_suppliers.json")
        print("💾 All data saved successfully!")
        self.close_driver()

    def parse_page(self, query) -> list:
        """Extracts supplier details from IndiaMART search results."""
        suppliers = []
        scroll_attempts = 0

        while len(suppliers) < self.MIN_SUPPLIERS and scroll_attempts < self.SCROLL_LIMIT:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            print(f"✅ Scrolled to the bottom (Attempt {scroll_attempts + 1})")

            # Click "Show more results" if available
            try:
                show_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'showmoreresultsdiv')]/button"))
                )
                show_more_button.click()
                time.sleep(3)
                print("📩 Clicked 'Show more results'")
            except Exception:
                print("⚠️ No 'Show more results' button found.")

            scroll_attempts += 1

        print("✅ Extracting supplier details...")

        try:
            supplier_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )
        except Exception:
            print(f"⚠️ No suppliers found for {query}!")
            return []

        print(f"🔍 Found {len(supplier_cards)} supplier cards for {query}")
        for idx, card in enumerate(supplier_cards):
            try:
                name = card.find_element(By.CLASS_NAME, "producttitle").text.strip()
                company = self.get_text_or_default(card, "companyname")
                price = self.get_text_or_default(card, "price")
                website = self.get_attribute_or_default(card, "a", "href")

                supplier_info = {
                    "product": query,
                    "name": name,
                    "company": company,
                    "price": price,
                    "website": website,
                    "country": "India",
                    "industries": ["General Manufacturing"],
                    "processes": ["Unknown"],
                    "certifications": ["Unknown"],
                    "customers": ["Unknown"],
                    "employees": "Unknown",
                    "revenue": "Unknown"
                }

                self.save_data([supplier_info], "indiamart_suppliers.json")
                suppliers.append(self.standardize_data(supplier_info))
            except Exception as e:
                print(f"⚠️ Skipping supplier {idx + 1} due to error: {e}")
        return suppliers

    def save_data(self, data, filename):
        """Saves data to a JSON file, overwriting any existing data."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"💾 Data saved successfully in {filename}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")

    def get_text_or_default(self, element, class_name, default="N/A"):
        """Returns text of an element or default if not found."""
        found_elements = element.find_elements(By.CLASS_NAME, class_name)
        return found_elements[0].text.strip() if found_elements else default

    def get_attribute_or_default(self, element, tag_name, attribute, default="N/A"):
        """Returns attribute value of an element or default if not found."""
        found_elements = element.find_elements(By.TAG_NAME, tag_name)
        return found_elements[0].get_attribute(attribute) if found_elements else default


if __name__ == "__main__":
    search_terms = ["steel manufacturers"]
    custom_urls = []  # Example: ["https://dir.indiamart.com/example-url"]
    scraper = IndiaMARTScraper(search_terms, custom_urls)
    scraper.run_scraper()
