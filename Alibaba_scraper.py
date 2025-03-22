from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseScraper import BaseScraper
import json
import os

class AlibabaScraper(BaseScraper):
    """Scraper for extracting supplier data from Alibaba."""

    BASE_URL = "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={query}"

    def __init__(self, search_queries):
        super().__init__()
        self.search_queries = search_queries
        self.all_suppliers = []

    def run_scraper(self):
        """Runs the scraper for multiple product searches."""
        for query in self.search_queries:
            search_url = self.BASE_URL.format(query=query.replace(" ", "+"))
            print(f"\n🔍 Searching: {query}")
            print(f"🌐 URL: {search_url}")

            self.fetch_page(search_url)
            supplier_data = self.parse_page(query)
            print(f"📦 Extracted {len(supplier_data)} suppliers for {query}")
            self.all_suppliers.extend(supplier_data)

        self.save_data(self.all_suppliers, "alibaba_suppliers.json")
        print("💾 All data saved successfully!")
        self.close_driver()

    def parse_page(self, query) -> list:
        """Extracts supplier details from Alibaba search results."""
        suppliers = []
        print("✅ Extracting supplier details...")

        try:
            supplier_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fy23-search-card"))
            )
        except Exception:
            print(f"⚠️ No suppliers found for {query}!")
            return []

        print(f"🔍 Found {len(supplier_cards)} supplier cards for {query}")
        for idx, card in enumerate(supplier_cards):
            try:
                name = self.get_text_or_default(card, "data-spm", "d_title")
                company = self.get_text_or_default(card, "search-card-e-company")
                price = self.get_text_or_default(card, "search-card-e-price-main")
                website = self.get_attribute_or_default(card, "a", "href")
                reviews = self.get_text_or_default(card, "search-card-e-review")

                supplier_info = {
                    "product": query,
                    "name": company,
                    "company": company,
                    "price": price,
                    "website": "https://www.alibaba.com" + website if website.startswith("//") else website,
                    "reviews": reviews,
                    "country": "Unknown",
                    "industries": ["General Manufacturing"],
                    "processes": ["Unknown"],
                    "certifications": ["Unknown"],
                    "customers": ["Unknown"],
                    "employees": "Unknown",
                    "revenue": "Unknown"
                }

                self.save_data([supplier_info], "alibaba_suppliers.json")
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
    scraper = AlibabaScraper(search_terms)
    scraper.run_scraper()
