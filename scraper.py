import time
import threading
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go


# Lista symboli
asset_list = ["EURUSD","GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
request_counter = 0
last_request_time = None 

# Słowniki do przechowywania danych dla każdego symbolu
time_stamps = {asset: [] for asset in asset_list}
long_values = {asset: [] for asset in asset_list}
short_values = {asset: [] for asset in asset_list}

current_values = {asset: {"long": None, "short": None} for asset in asset_list}

def update_all_plots():
    for asset in asset_list:
        fig = go.Figure()

        # Wykres długich pozycji
        fig.add_trace(go.Scatter(
            x=time_stamps[asset],
            y=long_values[asset],
            mode='lines+markers+text',
            name=f"{asset} Long (%)",
            line=dict(color='lime'),
            marker=dict(size=8),
            #text=[f"{val}%" for val in long_values[asset]],
            #textposition="top center",
            hovertemplate="Long: %{y:.1f}%" 
        ))

        # Wykres krótkich pozycji
        fig.add_trace(go.Scatter(
            x=time_stamps[asset],
            y=short_values[asset],
            mode='lines+markers+text',
            name=f"{asset} Short (%)",
            line=dict(color='red'),
            marker=dict(size=8),
            #text=[f"{val}%" for val in short_values[asset]],
            #textposition="top center",
            hovertemplate="Short: %{y:.1f}%"
        ))

        # Stylizacja wykresu
        fig.update_layout(       
            #title=f"{asset} Sentiment Over Time",
            xaxis_title="Time (HH:MM)",
            yaxis_title="Percentage (%)",
            paper_bgcolor="#1f1f1f",
            plot_bgcolor="#2d2d2d",
            font=dict(color="white"),
            margin=dict(l=20, r=20, t=20, b=20),
            #height=600,  # Podstawowa wysokość
            #width="100%",  # Pełna szerokość
            yaxis=dict(
                range=[-5, 105],  # Zakres osi Y od -5% do 105%
                tickmode='linear',
                dtick=10,  # Oznaczenia co 10%
                showgrid=True,  # Widoczna siatka
                zeroline=False  # Wyłączenie linii zerowej
            ),
            autosize=True,  # Wyłączenie automatycznego rozmiaru
        )


        # Generowanie pliku HTML z osadzeniem pełnego stylu div
        html_code = fig.to_html(full_html=False, include_plotlyjs="cdn")
        html_code = html_code.replace(
            '<div id="',
            '<div style="width: 100%; height: 100%;" id="'
        )

        with open(f"/tmp/{asset}_plot.html", "w") as f:
            f.write(html_code)
    
def run_scraper():
    print("[INFO] Scraper został uruchomiony!")
    global request_counter
    global last_request_time

    for asset in asset_list:
        url = f"https://www.myfxbook.com/community/outlook/{asset}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers)
            request_counter += 1  # Zwiększamy licznik przy każdym zapytaniu
            response.raise_for_status()

            print(f"[INFO] Request do {url} zakończony sukcesem! Status Code: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            table_rows = soup.find_all('tr')

            new_long = None
            new_short = None

            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    if 'Long' in cells[0].text.strip():
                        new_long = int(cells[1].text.strip().replace('%', ''))
                    elif 'Short' in cells[0].text.strip():
                        new_short = int(cells[1].text.strip().replace('%', ''))

            if new_long is not None and new_short is not None:
                current_time = datetime.now().strftime("%H:%M")
                print(f"[INFO] {asset} - Long: {new_long}%, Short: {new_short}%, Czas: {current_time}")
                time_stamps[asset].append(current_time)
                long_values[asset].append(new_long)
                short_values[asset].append(new_short)
            else:
                print(f"[WARNING] Nie znaleziono danych dla {asset}")

        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] Błąd HTTP dla {asset}: {http_err}")
        except Exception as e:
            print(f"[ERROR] Inny błąd dla {asset}: {e}")

    last_request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_all_plots()
    time.sleep(300)

if __name__ == "__main__":
    run_scraper()
