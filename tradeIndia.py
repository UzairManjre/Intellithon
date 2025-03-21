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

class TradeIndiaScraper(BaseScraper):
    """Scraper for extracting supplier data from TradeIndia."""

    def __init__(self, search_query):
        super().__init__()
        self.base_url = "https://www.tradeindia.com/"
        self.search_query = search_query
        self.scraped_data = []

    def run_scraper(self):
        """Runs the scraper: fetch, parse, and save data across multiple pages."""
        page_num = 1
        self.scraped_data = []

        while True:
            search_url = f"https://www.tradeindia.com/search.html?keyword={self.search_query}&page={page_num}"
            self.fetch_page(search_url)
            
            supplier_data = self.parse_page()
            if not supplier_data:  # Stop if no more suppliers found
                break
            
            self.scraped_data.extend(supplier_data)
            
            for index, supplier in enumerate(supplier_data, 1):
                print(f"\nSupplier {index + len(self.scraped_data) - len(supplier_data)}:")
                for key, value in supplier.items():
                    if isinstance(value, dict):  # Handling metadata separately
                        print(f"  {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"    {sub_key}: {sub_value}")
                    else:
                        print(f"{key}: {value}")
            
            print(f"Scraped Page {page_num}, Total Suppliers: {len(self.scraped_data)}")
            
            # Check if there is a next page button
            next_page_element = self.driver.find_elements(By.CLASS_NAME, "highlight_btn")
            if not next_page_element:
                break  # Stop if no next page
            
            page_num += 1

        self.save_data(self.scraped_data, "trade_india_suppliers.json")
        self.close_driver()


    def parse_page(self) -> list[dict]:
        """Extracts supplier details from TradeIndia search results."""
        suppliers = []
        suppliers.append({
            "Company Name": "svm pvt ltd",
            "Website": "website",
            "Country": "India",  # Since it's TradeIndia
            "Industries Served": ["General Manufacturing"],  # Placeholder
            "Manufacturing Processes": ["Unknown"],  # Placeholder
            "Certifications": ["Unknown"],  # Placeholder
            "Customers": ["Unknown"],  # Placeholder
            "Metadata": {
                "# Employees": "Unknown",
                "Annual Revenue": "Unknown"
            }
        })


        # Wait for elements to load
        time.sleep(3)

        # Verify the correct selector (update if TradeIndia changes their site structure)<h2 color="#2D3840" class="sc-3b1eb120-11 RqywW mb-1 card_title Body3R">Wire For Central Wheels - Size: Standard</h2>
        try:
            supplier_cards = self.driver.find_elements(By.CLASS_NAME, "card")  
        except Exception as e:
            print(f"Error fetching supplier cards: {e}")
            return []

        for card in supplier_cards:
            try:
                prod_element = card.find_element(By.CLASS_NAME, "sc-3b1eb120-11")
                prod_name = prod_element.text if prod_element else "Unknown"

                # Extract company name
                company_element = card.find_element(By.CLASS_NAME, "sc-3b1eb120-13")
                company_name = company_element.text if company_element else "Unknown"


                # Extract website URL
                website_element = card.find_elements(By.TAG_NAME, "a")
                website = website_element[0].get_attribute("href") if website_element else "N/A"

                suppliers.append({
                    "Product Name": prod_name,
                    "Company Name": company_name,
                    "Website": website,
                    "Country": "India",  # Since it's TradeIndia
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
    

    def get_next_page_url(self):
        """Finds and returns the URL of the next page, if available."""
        try:
            next_button = self.driver.find_element(By.CLASS_NAME, "highlight_btn")  # Update if needed
            next_page_url = next_button.get_attribute("href")
            return next_page_url
        except Exception:
            return None  # No next page found
    


if __name__ == "__main__":
    search_term = "steel manufacturers"
    scraper = TradeIndiaScraper(search_term)
    scraper.run_scraper()


