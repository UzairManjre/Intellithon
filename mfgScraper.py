from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

class BaseScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Ensure you have the correct WebDriver installed

    def fetch_page(self, url):
        self.driver.get(url)
        time.sleep(5)  # Adjust sleep time as needed for the page to load

    def save_data(self, data, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def close_driver(self):
        self.driver.quit()

class mfgScraper(BaseScraper):
    def __init__(self, search_query, location):
        super().__init__()
        self.base_url = "https://www.mfg.com"
        self.search_query = search_query
        self.location = location
        self.scraped_data = []  # Store all scraped suppliers across pages

    def run_scraper(self):
        """Runs the scraper: fetch, parse, paginate, print, and save data."""
        search_url = f"https://www.mfg.com/manufacturer-directory/?manufacturing_location={self.location}&ep_filter_manufacturing_location={self.location}&capability={self.search_query}&ep_filter_capability={self.search_query}&search="
        self.fetch_page(search_url)

        while True:
            supplier_data = self.parse_page()
            self.scraped_data.extend(supplier_data)

            # Print extracted details for each batch of suppliers
            for index, supplier in enumerate(supplier_data, 1):
                print(f"\nSupplier {index + len(self.scraped_data) - len(supplier_data)}:")
                for key, value in supplier.items():
                    if isinstance(value, dict):  # Handling metadata separately
                        print(f"  {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"    {sub_key}: {sub_value}")
                    else:
                        print(f"  {key}: {value}")

            # Stop if less than 25 suppliers are scraped on this page (end of pagination)
            if len(supplier_data) < 25:
                print("No more suppliers to scrape. Ending process.")
                break

            # Try moving to the next page
            next_page_url = self.get_next_page_url()
            if not next_page_url:
                print("Next page not found. Ending process.")
                break

            print(f"Moving to next page: {next_page_url}")
            self.fetch_page(next_page_url)  # Navigate to the next page

        # Save the extracted data
        self.save_data(self.scraped_data, "mfg_suppliers.json")
        self.close_driver()

    def parse_page(self) -> list[dict]:
        """Extracts supplier details from MFG search results."""
        suppliers = []
        
        supplier_cards = self.driver.find_elements(By.CLASS_NAME, "bg-white.container.hover-glow.p-4.mb-3")
        
        for card in supplier_cards:
            try:
                name = card.find_element(By.CLASS_NAME, "align-text-bottom").text
                
                # Find the "View More Details" button link
                website_element = card.find_elements(By.CSS_SELECTOR, "a.button.w-100")
                website = (
                    f"{self.base_url}{website_element[0].get_attribute('href')}"
                    if website_element
                    else "N/A"
                )
                
                suppliers.append({
                    "Company Name": name,
                    "Website": website,
                    "Country": self.location,  
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

    def get_next_page_url(self) -> str:
        """Extracts the 'Next' page URL from pagination if available."""
        try:
            pagination = self.driver.find_element(By.CLASS_NAME, "justify-content-center.pagination")
            next_button = pagination.find_elements(By.XPATH, ".//a[contains(text(),'Next')]")
            
            if next_button:
                return next_button[0].get_attribute("href")  # Extract the URL

        except Exception as e:
            print(f"Error finding next page: {e}")

        return None  # No next page found

if __name__ == "__main__":
    search_query = "welding"
    scraper = mfgScraper(search_query, "United States")
    scraper.run_scraper()
    