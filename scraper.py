import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Grupy assetów
assets1 = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
assets2 = ["USDCAD", "EURAUD", "EURJPY", "AUDJPY", "AUDNZD"]
assets3 = ["CADJPY", "EURCHF", "EURGBP", "GBPCAD", "CADCHF"]

all_assets = assets1 + assets2 + assets3

# Dane do wykresów
time_stamps = {asset: [] for asset in all_assets}
long_values = {asset: [] for asset in all_assets}
short_values = {asset: [] for asset in all_assets}
last_update_times = {f"group{i}": None for i in range(1, 4)}

def run_scraper():
    while True:
        # Aktualizacja kolejnych grup
        for i, assets in enumerate([assets1, assets2, assets3], 1):
            print(f"[INFO] Aktualizacja grupy {i}: {assets}")
            last_update_times[f"group{i}"] = datetime.now().strftime("%H:%M:%S")
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

            # Odczekaj 5 minut przed kolejną grupą
            time.sleep(300)
