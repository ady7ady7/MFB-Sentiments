import requests
from bs4 import BeautifulSoup

# Lista symboli do przetestowania
asset_list = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]

def test_requests():
    for asset in asset_list:
        url = f"https://www.myfxbook.com/community/outlook/{asset}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        print(f"\n[INFO] Wysyłanie requestu do: {url}")
        try:
            # Wysyłanie requestu
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Szczegóły odpowiedzi
            print(f"[INFO] Status Code: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Szukanie wartości Long i Short w tabeli
            table_rows = soup.find_all('tr')
            long_percentage = None
            short_percentage = None

            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    if 'Long' in cells[0].text.strip():
                        long_percentage = cells[1].text.strip()
                    elif 'Short' in cells[0].text.strip():
                        short_percentage = cells[1].text.strip()

            # Wyświetlenie wyników
            if long_percentage and short_percentage:
                print(f"[RESULT] {asset} - Long: {long_percentage}, Short: {short_percentage}")
            else:
                print(f"[WARNING] Nie znaleziono wartości Long/Short dla {asset}.")

        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] Błąd HTTP dla {asset}: {http_err}")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Problem z połączeniem z {url}")
        except requests.exceptions.Timeout:
            print(f"[ERROR] Przekroczono czas oczekiwania na odpowiedź z {url}")
        except Exception as e:
            print(f"[ERROR] Inny błąd: {e}")

if __name__ == "__main__":
    test_requests()

