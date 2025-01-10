import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Lista symboli
asset_list = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
request_counter = 0
last_request_time = None

# Dane do wykresów
time_stamps = {asset: [] for asset in asset_list}
long_values = {asset: [] for asset in asset_list}
short_values = {asset: [] for asset in asset_list}

def run_scraper():
    global request_counter
    global last_request_time

    while True:
        for asset in asset_list:
            url = f"https://www.myfxbook.com/community/outlook/{asset}"
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                response = requests.get(url, headers=headers)
                request_counter += 1  # Zwiększamy licznik przy każdym zapytaniu
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
                    print(f"[WARNING] Nie znaleziono danych dla {asset}.")

            except requests.exceptions.HTTPError as http_err:
                print(f"[ERROR] Błąd HTTP dla {asset}: {http_err}")
            except Exception as e:
                print(f"[ERROR] Inny błąd dla {asset}: {e}")

        last_request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(300)  # 5 minut przerwy

