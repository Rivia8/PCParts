# PC Part Price Scraper 🖥️

A simple and effective web application built with Python and Flask to scrape real-time pricing for PC components from major UK retailers. This project was created to automate and streamline the process of finding the best deals for custom PC builds.

---

## 🚀 Key Features

- **Multi-Website Scraping:** Gathers data from several top UK PC part websites (e.g., Scan, Overclockers UK, CCL).
- **Real-Time Data:** Fetches the most current prices on every search, ensuring accuracy.
- **Clean & Simple UI:** Displays the scraped data in a clean, easy-to-read table.
- **Find the Best Deals:** Quickly identify the cheapest retailer for any given component.

---

## 🛠️ Tech Stack

- **Backend:** Python
- **Web Framework:** Flask
- **Web Scraping:** BeautifulSoup4, Requests
- **Frontend:** HTML, TAILWINDCSS

---

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

**1. Prerequisites:**
   - Ensure you have [Python 3.8+](https://www.python.org/downloads/) installed.
   - You will also need `pip` for installing packages.

**2. Clone the Repository:**
   ```bash
   git clone [https://github.com/Rivia8/PCParts.git](https://github.com/Rivia8/PCParts.git)
   cd PCParts
   ```

**3. Create a Virtual Environment:**
   It's highly recommended to use a virtual environment to keep dependencies isolated.
   ```bash
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

**4. Install Dependencies:**
   Install all the required packages from the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you haven't created a `requirements.txt` file yet, you can do so by running `pip freeze > requirements.txt` after installing your packages (like Flask, BeautifulSoup4, etc.).*

**5. Run the Application:**
   Start the Flask development server.
   ```bash
   flask run
   ```
   The application should now be running at `http://127.0.0.1:5000`.

---

## Usage

Once the application is running, open your web browser and navigate to `http://127.0.0.1:5000`. Enter the name of the PC component you wish to search for (e.g., "Nvidia RTX 4070" or "AMD Ryzen 7 7800X3D") and the application will return a table of current prices from the supported websites.

---
