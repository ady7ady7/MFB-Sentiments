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
            print(f"[INFO] Nagłówki odpowiedzi:\n{response.headers}")
            print(f"[INFO] Czas odpowiedzi: {response.elapsed.total_seconds()} sekund")
            print(f"[INFO] Długość treści odpowiedzi: {len(response.text)} znaków")
            print(f"[INFO] Podgląd treści HTML (pierwsze 500 znaków):\n{response.text[:500]}")

            # Parsowanie HTML (sprawdzenie, czy struktura tabeli istnieje)
            soup = BeautifulSoup(response.text, 'html.parser')
            table_rows = soup.find_all('tr')

            if table_rows:
                print(f"[INFO] Znaleziono {len(table_rows)} wierszy w tabeli.")
            else:
                print(f"[WARNING] Brak wierszy tabeli dla {asset}. Struktura HTML może być inna.")

        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] Błąd HTTP: {http_err}")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Problem z połączeniem z {url}")
        except requests.exceptions.Timeout:
            print(f"[ERROR] Przekroczono czas oczekiwania na odpowiedź z {url}")
        except Exception as e:
            print(f"[ERROR] Inny błąd: {e}")

if __name__ == "__main__":
    test_requests()
