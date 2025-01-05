from flask import Flask, render_template, jsonify
from threading import Thread
import scraper
import time

app = Flask(__name__)

def scraper_loop():
    while True:
        print("[INFO] Uruchamianie scrapera...")
        scraper.run_scraper()
        time.sleep(300)  # Odczekaj 5 minut przed ponownym uruchomieniem

@app.before_first_request
def start_scraper():
    print("[INFO] Scraper uruchomiony przed pierwszym requestem")
    Thread(target=scraper_loop, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html", assets=scraper.asset_list, refresh_minutes=5)

@app.route("/status")
def status():
    return jsonify({
        "last_update": scraper.last_request_time,
        "refresh_interval": 5  # Interwał odświeżania w minutach
    })

if __name__ == "__main__":
    app.run(debug=True)
