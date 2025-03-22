from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for key features page
@app.route('/key-features')
def key_features():
    return render_template('key-features.html')

# Route for industries page
@app.route('/industries')
def industries():
    return render_template('industries.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for login/signup page
@app.route('/login')
def login():
    return render_template('login.html')

# Sample scraper API (Replace with your actual scrapers)
@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    search_query = data.get('query', '')
    # Placeholder for scraper function
    scraped_data = {"message": f"Scraping data for {search_query}..."}
    return jsonify(scraped_data)



if __name__ == '__main__':
    app.run(debug=True)
