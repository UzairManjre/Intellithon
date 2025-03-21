from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    item = None
    country = None
    min_price = None
    max_price = None

    if request.method == "POST":
        item = request.form.get("item")
        country = request.form.get("country")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")

    return render_template("index.html", item=item, country=country, min_price=min_price, max_price=max_price)

if __name__ == "__main__":
    app.run(debug=True)
