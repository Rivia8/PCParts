from flask import Flask, render_template, request
from scraper import find_scan_prices

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    prices = []
    query = ""

    # Only runs when the user submits the form
    if request.method == 'POST':
        query = request.form.get('user_text', '')
        if query:
            # Returns a list of prices
            prices = find_scan_prices(query)
        
    return render_template("index.html", prices = prices, query=query)

if __name__ == "__main__":
    app.run(debug=True)
