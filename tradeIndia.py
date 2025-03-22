from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time


class BaseScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def fetch_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def save_data(self, data, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def clear_data(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    def close_driver(self):
        self.driver.quit()


class TradeIndiaScraper(BaseScraper):
    def __init__(self, search_query, max_suppliers=200):
        super().__init__()
        self.base_url = "https://www.tradeindia.com/"
        self.search_query = search_query
        self.scraped_data = []
        self.data_filename = "trade_india_suppliers.json"
        self.max_suppliers = max_suppliers

    def run_scraper(self):
        self.clear_data(self.data_filename)
        page_num = 1
        total_scraped = 0

        while total_scraped < self.max_suppliers:
            search_url = f"https://www.tradeindia.com/search.html?keyword={self.search_query}&page={page_num}"
            self.fetch_page(search_url)

            supplier_data = self.parse_page()
            if not supplier_data:
                break  # Stop if no more suppliers found

            available_space = self.max_suppliers - total_scraped
            supplier_data = supplier_data[:available_space]  # Limit suppliers if max reached

            self.scraped_data.extend(supplier_data)
            self.save_data(self.scraped_data, self.data_filename)

            for index, supplier in enumerate(supplier_data, 1):
                print(f"\nSupplier {index + total_scraped}:")
                for key, value in supplier.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"    {sub_key}: {sub_value}")
                    else:
                        print(f"{key}: {value}")

            total_scraped += len(supplier_data)
            print(f"Scraped Page {page_num}, Total Suppliers: {total_scraped}")

            if total_scraped >= self.max_suppliers or not self.get_next_page_url():
                break  # Stop if limit is reached or no next page

            page_num += 1

        self.close_driver()

    def parse_page(self) -> list[dict]:
        suppliers = []
        time.sleep(3)

        try:
            supplier_cards = self.driver.find_elements(By.CLASS_NAME, "card")
        except Exception as e:
            print(f"Error fetching supplier cards: {e}")
            return []

        for card in supplier_cards:
            try:
                prod_element = card.find_element(By.CLASS_NAME, "sc-3b1eb120-11")
                prod_name = prod_element.text if prod_element else "Unknown"

                company_element = card.find_element(By.CLASS_NAME, "sc-3b1eb120-13")
                company_name = company_element.text if company_element else "Unknown"

                website_element = card.find_elements(By.TAG_NAME, "a")
                website = website_element[0].get_attribute("href") if website_element else "N/A"

                suppliers.append({
                    "Product Name": prod_name,
                    "Company Name": company_name,
                    "Website": website,
                    "Country": "India",
                    "Industries Served": ["General Manufacturing"],
                    "Manufacturing Processes": ["Unknown"],
                    "Certifications": ["Unknown"],
                    "Customers": ["Unknown"],
                    "Metadata": {
                        "# Employees": "Unknown",
                        "Annual Revenue": "Unknown"
                    }
                })

            except Exception as e:
                print(f"Skipping a supplier due to error: {e}")

        return suppliers

    def get_next_page_url(self):
        try:
            next_button = self.driver.find_element(By.CLASS_NAME, "highlight_btn")
            return next_button.get_attribute("href")
        except Exception:
            return None


if __name__ == "__main__":
    search_term = "steel manufacturers"
     # Set maximum supplier limit
    scraper = TradeIndiaScraper(search_term)
    scraper.run_scraper()
