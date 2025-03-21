from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time


class BaseScraper:
    """Abstract class for all supplier scrapers."""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without UI
        self.driver = webdriver.Chrome(service=Service("path_to_chromedriver"), options=chrome_options)

    def fetch_page(self, url: str) -> str:
        """Fetches page source."""
        self.driver.get(url)
        time.sleep(3)  # Let page load
        return self.driver.page_source

    def parse_page(self, html: str) -> list[dict]:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement parse_page")

    def save_data(self, data: list[dict], filename: str):
        """Saves data in JSON format."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

    def standardize_data(self, raw_data: dict) -> dict:
        """Ensures all extracted supplier data follows a standard structure."""
        return {
            "Company Name": raw_data.get("name", "N/A"),
            "Website": raw_data.get("website", "N/A"),
            "Country": raw_data.get("country", "N/A"),
            "Industries Served": raw_data.get("industries", []),
            "Manufacturing Processes": raw_data.get("processes", []),
            "Certifications": raw_data.get("certifications", []),
            "Customers": raw_data.get("customers", []),
            "Metadata": {
                "# Employees": raw_data.get("employees", "N/A"),
                "Annual Revenue": raw_data.get("revenue", "N/A"),
            }
        }

    def close_driver(self):
        """Closes the browser session."""
        self.driver.quit()
