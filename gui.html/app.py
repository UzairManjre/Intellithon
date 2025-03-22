from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

from Alibaba_scraper import AlibabaScraper
from IndiaMARTScraper import IndiaMARTScraper
from mfgScraper import mfgScraper
from tradeIndia import TradeIndiaScraper
import Ai_model

app = Flask(__name__)
app.secret_key = "your_secret_key"

SUPPLIER_JSON_PATH = "output.json"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/key_features')
def key_features():
    return render_template('key-features.html')

@app.route('/industries')
def industries():
    return render_template('industries.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/search', methods=['POST'])
def search():
    product_name = request.form.get('query', '').strip().lower()
    country = request.form.get('country', '').strip().lower()

    # Run scrapers before searching the database
    run_scrapers(product_name, country)

    if not os.path.exists(SUPPLIER_JSON_PATH):
        return "No supplier data found.", 404

    with open(SUPPLIER_JSON_PATH, 'r') as json_file:
        suppliers = json.load(json_file)

    filtered_suppliers = [
        supplier for supplier in suppliers
        if product_name in supplier.get("product", "").lower()
        and country in supplier.get("location", "").lower()
    ]

    with open("filtered_suppliers.json", "w") as temp_file:
        json.dump(filtered_suppliers, temp_file, indent=4)

    return redirect(url_for('results', page=1))

def run_scrapers(product_name, country):
    """Call the scrapers and update output.json"""
    print("Running scrapers...")

    alibaba_scraper = AlibabaScraper([product_name])
    alibaba_scraper.run_scraper()

    mfg_scraper = mfgScraper(product_name, country)
    mfg_scraper.run_scraper()
    tradeIndia = TradeIndiaScraper(product_name)
    tradeIndia.run_scraper()
    scraper = IndiaMARTScraper([product_name])
    scraper.run_scraper()

    print("Scrapers finished.")
    Ai_model.main()



@app.route('/results/<int:page>')
def results(page):
    if not os.path.exists(SUPPLIER_JSON_PATH):
        return "No search results. Please perform a search first.", 404

    with open(SUPPLIER_JSON_PATH, "r") as temp_file:
        suppliers = json.load(temp_file)

    if not suppliers:
        return "No matching suppliers found.", 404

    per_page = 25
    total_pages = (len(suppliers) + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        return "Invalid page number.", 400

    suppliers_to_display = suppliers[(page - 1) * per_page: page * per_page]

    return render_template('result.html',
                           suppliers=suppliers_to_display,
                           page=page,
                           total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
