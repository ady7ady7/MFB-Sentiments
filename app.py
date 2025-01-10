from flask import Flask, render_template, jsonify
import threading
import scraper

app = Flask(__name__)

# Uruchomienie scrapera w tle
def start_scraper():
    threading.Thread(target=scraper.run_scraper, daemon=True).start()

start_scraper()  # Scraper uruchamiany przy starcie aplikacji

@app.route("/")
def index():
    print(f"[DEBUG] Aktualne dane przekazywane do widoku: {scraper.current_values}")
    return render_template("index.html", assets=scraper.asset_list, current_values=scraper.current_values)


@app.route("/status")
def status():
    return jsonify({
        "last_update": scraper.last_request_time
    })

@app.route("/debug")
def debug():
    return jsonify(scraper.current_values)


if __name__ == "__main__":
    app.run(debug=True)
