from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time

from webdriver_manager.chrome import ChromeDriverManager


class BaseScraper:
    """Abstract class for all supplier scrapers."""

    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Explicitly set Chrome path

        # Key flags to avoid DevTools issue
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")  # Enable debugging port
        chrome_options.add_argument("--disable-extensions")  # Avoid extension conflicts
        chrome_options.add_argument("--disable-software-rasterizer")  # Fix rendering crashes
        chrome_options.add_argument("--disable-background-networking")
        # Load existing user profile to retain login credentials
        chrome_options.add_argument("--user-data-dir=C:/Users/uzair/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("--profile-directory=Default")  # Change if needed (e.g., "Profile 1")

        # Optional: Run in headless mode to avoid UI interference
        chrome_options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    def fetch_page(self, url: str) -> str:
        """Fetches page source."""
        try:
            self.driver.get(url)
            time.sleep(3)  # Let page load
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching page: {e}")
            return ""

    def parse_page(self, html: str) -> list[dict]:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement parse_page")

    def save_data(self, data: list[dict], filename: str):
        """Saves data in JSON format."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

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
        if self.driver:
            try:
                self.driver.quit()
                print("Browser session closed successfully.")
            except Exception as e:
                print(f"Error closing browser: {e}")
