from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

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

    if not os.path.exists(SUPPLIER_JSON_PATH):
        return "No supplier data found.", 404

    with open(SUPPLIER_JSON_PATH, 'r') as json_file:
        suppliers = json.load(json_file)

    # Filter suppliers based on search criteria
    filtered_suppliers = [
        supplier for supplier in suppliers
        if product_name in supplier.get("product", "").lower()
        and country in supplier.get("location", "").lower()
    ]

    # Save filtered results in a temporary JSON file
    with open("filtered_suppliers.json", "w") as temp_file:
        json.dump(filtered_suppliers, temp_file, indent=4)

    return redirect(url_for('results', page=1))


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


@app.route('/results/<int:page>')
def filtered_results(page):
    if not os.path.exists(SUPPLIER_JSON_PATH):
        return "No suppliers found. Please perform a search first.", 404

    with open(SUPPLIER_JSON_PATH, 'r') as json_file:
        suppliers = json.load(json_file)

    per_page = 25
    total_pages = (len(suppliers) + per_page - 1) // per_page
    suppliers_to_display = suppliers[(page - 1) * per_page: page * per_page]

    return render_template('result.html', suppliers=suppliers_to_display, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
