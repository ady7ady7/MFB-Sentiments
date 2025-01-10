import os
from flask import Flask, render_template, jsonify
import threading
import scraper

app = Flask(__name__)

def start_scraper():
    threading.Thread(target=scraper.run_scraper, daemon=True).start()

start_scraper()

@app.route("/")
def index():
    return render_template("index.html", assets=scraper.asset_list, current_values=scraper.current_values)

@app.route("/status")
def status():
    return jsonify({
        "last_update": scraper.last_request_time
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pobierz port ze zmiennej środowiskowej lub użyj domyślnie 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # Host 0.0.0.0, aby nasłuchiwać na wszystkie adresy

