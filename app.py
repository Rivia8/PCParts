from flask import Flask, render_template, request
from scraper import get_all_products

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/newparts", methods=['GET', 'POST'])
def new_parts():
    products = []
    query = ""

    # Only runs when the user submits the form
    if request.method == 'POST':
        query = request.form.get('user_text', '')
        if query:
            # Returns a list of products
            products = get_all_products(query)
        
    return render_template("NewParts.html", products = products, query=query)

if __name__ == "__main__":
    app.run(debug=True)
