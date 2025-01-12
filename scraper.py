import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading

# Trzy grupy assetów
assets1 = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
assets2 = ["USDCAD", "EURAUD", "EURJPY", "AUDJPY", "AUDNZD"]
assets3 = ["CADJPY", "EURCHF", "EURGBP", "GBPCAD", "CADCHF"]

all_assets = assets1 + assets2 + assets3

# Dane do wykresów
time_stamps = {asset: [] for asset in all_assets}
long_values = {asset: [] for asset in all_assets}
short_values = {asset: [] for asset in all_assets}
last_request_time = None

# Funkcja scrapująca dla danej listy assetów
def run_scraper_for_assets(assets, delay_between_requests=0):
    global last_request_time

    while True:
        for asset in assets:
            url = f"https://www.myfxbook.com/community/outlook/{asset}"
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

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
                    time_stamps[asset].append(current_time)
                    long_values[asset].append(new_long)
                    short_values[asset].append(new_short)
                    print(f"[INFO] {asset} - Long: {new_long}%, Short: {new_short}%")
                else:
                    print(f"[WARNING] Brak danych dla {asset}.")

            except requests.exceptions.HTTPError as http_err:
                print(f"[ERROR] Błąd HTTP dla {asset}: {http_err}")
            except Exception as e:
                print(f"[ERROR] Inny błąd dla {asset}: {e}")

            # Opóźnienie między zapytaniami dla bezpieczeństwa
            time.sleep(delay_between_requests)

        last_request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(300)  # Przerwa 5 minut przed kolejną aktualizacją całej grupy assetów

