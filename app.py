from flask import Flask, render_template, request
from scraper import get_all_products

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/findparts", methods=['GET', 'POST'])
def new_parts():
    products = []
    query = ""

    # Only runs when the user submits the form
    if request.method == 'POST':
        query = request.form.get('user_text', '')

        is_used = 'used_parts_check' in request.form
        if query:
            # Returns a list of products
            products = get_all_products(query, is_used)
        
    return render_template("FindParts.html", products = products, query=query)

if __name__ == "__main__":
    app.run(debug=True)
