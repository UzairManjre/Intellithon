from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

from BaseScraper import BaseScraper


class IndiaMARTScraper(BaseScraper):
    """Scraper for extracting supplier data from IndiaMART."""

    def __init__(self, search_query):
        super().__init__()
        self.base_url = "https://www.indiamart.com"
        self.search_query = search_query

    def run_scraper(self):
        """Runs the scraper: fetch, parse, and save data."""
        search_url = f"{self.base_url}/search.mp?ss={self.search_query.replace(' ', '+')}"
        self.fetch_page(search_url)
        supplier_data = self.parse_page()
        self.save_data(supplier_data, "indiamart_suppliers.json")
        self.close_driver()

    def parse_page(self) -> list[dict]:
        """Extracts supplier details from IndiaMART search results."""
        suppliers = []

        supplier_cards = self.driver.find_elements(By.CLASS_NAME, "lst-cl")

        for card in supplier_cards:
            try:
                name = card.find_element(By.CLASS_NAME, "lcname").text
                website_element = card.find_elements(By.CLASS_NAME, "cmp-wt")
                website = website_element[0].get_attribute("href") if website_element else "N/A"

                suppliers.append({
                    "Company Name": name,
                    "Website": website,
                    "Country": "India",  # Since it's IndiaMART
                    "Industries Served": ["General Manufacturing"],  # Placeholder
                    "Manufacturing Processes": ["Unknown"],  # Placeholder
                    "Certifications": ["Unknown"],  # Placeholder
                    "Customers": ["Unknown"],  # Placeholder
                    "Metadata": {
                        "# Employees": "Unknown",
                        "Annual Revenue": "Unknown"
                    }
                })

            except Exception as e:
                print(f"Skipping a supplier due to error: {e}")

        return suppliers


if __name__ == "__main__":
    search_term = "steel manufacturers"
    scraper = IndiaMARTScraper(search_term)
    scraper.run_scraper()
