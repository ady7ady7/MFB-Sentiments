import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Lista symboli
asset_list = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
last_request_time = None

# Aktualne wartości do wyświetlania na stronie
current_values = {asset: {"long": "N/A", "short": "N/A"} for asset in asset_list}

def run_scraper():
    global last_request_time

    while True:
        for asset in asset_list:
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
                            new_long = cells[1].text.strip()
                        elif 'Short' in cells[0].text.strip():
                            new_short = cells[1].text.strip()

                if new_long and new_short:
                    current_values[asset] = {"long": new_long, "short": new_short}
                    print(f"[INFO] {asset} - Long: {new_long}, Short: {new_short}")
                else:
                    print(f"[WARNING] Brak danych dla {asset}.")

            except requests.exceptions.HTTPError as http_err:
                print(f"[ERROR] Błąd HTTP dla {asset}: {http_err}")
            except Exception as e:
                print(f"[ERROR] Inny błąd dla {asset}: {e}")

        last_request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(300)  # 5 minut przerwy

