import os
from flask import Flask, render_template, jsonify
import threading
import plotly.graph_objects as go
import scraper

app = Flask(__name__)

def start_all_scrapers():
    # Uruchamianie scraperów z różnymi opóźnieniami
    threading.Thread(target=scraper.run_scraper_for_assets, args=(scraper.assets1, 0), daemon=True).start()  # Bez opóźnienia
    threading.Thread(target=scraper.run_scraper_for_assets, args=(scraper.assets2, 0), daemon=True).start()  # 1.5 minuty opóźnienia
    threading.Thread(target=scraper.run_scraper_for_assets, args=(scraper.assets3, 0), daemon=True).start()  # 3 minuty opóźnienia

start_all_scrapers()

@app.route("/")
def index():
    return render_template("index.html", assets=scraper.all_assets)

@app.route("/get-plot-data/<asset>")
def get_plot_data(asset):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=scraper.time_stamps[asset],
        y=scraper.long_values[asset],
        mode='lines+markers',
        name=f"{asset} Long (%)",
        line=dict(color='lime')
    ))

    fig.add_trace(go.Scatter(
        x=scraper.time_stamps[asset],
        y=scraper.short_values[asset],
        mode='lines+markers',
        name=f"{asset} Short (%)",
        line=dict(color='red')
    ))

    fig.update_layout(
        xaxis_title="Czas (HH:MM)",
        yaxis_title="Procenty (%)",
        paper_bgcolor="#121212",
        plot_bgcolor="#2d2d2d",
        font=dict(color="white"),
        autosize=True,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(range=[-5, 105], tickmode='linear', dtick=10, showgrid=True, zeroline=False
    )

    return fig.to_json()

@app.route("/status")
def status():
    return jsonify({
        "last_update": scraper.last_request_time
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pobieranie portu ze zmiennej środowiskowej lub domyślnie 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # Nasłuch na 0.0.0.0 dla wszystkich adresów sieciowych

