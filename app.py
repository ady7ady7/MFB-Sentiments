from flask import Flask, render_template, jsonify
import threading
import scraper

app = Flask(__name__)

def start_scraper():
    threading.Thread(target=scraper.run_scraper, daemon=True).start()

@app.before_first_request
def start():
    start_scraper()

@app.route("/")
def index():
    return render_template("index.html", assets=scraper.asset_list, refresh_minutes=5, current_values=scraper.current_values)

@app.route("/status")
def status():
    return jsonify({
        "last_update": scraper.last_request_time,
        "refresh_interval": 5
    })

if __name__ == "__main__":
    app.run(debug=True)
