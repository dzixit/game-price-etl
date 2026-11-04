import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://api.isthereanydeal.com/games/history/v2"

GAME_ID = "018d937f-1ae9-734c-ba47-bd357cf07edd"
COUNTRY = "US"
SINCE = "2017-01-01T00:00:00Z"


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("ITAD_API_KEY", "").strip()

    if not api_key:
        print("Brak klucza API w konfiguracji.")
        return 1

    params = {
        "id": GAME_ID,
        "country": COUNTRY,
        "since": SINCE,
    }

    headers = {
        "ITAD-API-Key": api_key,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=30,
        )

        print(f"Status HTTP: {response.status_code}")
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("Przekroczono czas oczekiwania na API.")
        return 1

    except requests.exceptions.HTTPError:
        print("API zwróciło błąd. Sprawdź wyświetlony status HTTP.")
        return 1

    except requests.exceptions.RequestException:
        print("Nie udało się wykonać zapytania do API.")
        return 1

    # Zachowujemy odpowiedź przed analizą jej zawartości.
    raw_dir = PROJECT_ROOT / "data" / "raw"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_path = raw_dir / f"history_{GAME_ID}_{COUNTRY}_{timestamp}.json"

    try:
        raw_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
    except OSError:
        print("Nie udało się zapisać odpowiedzi do pliku.")
        return 1

    print(f"Zapisano odpowiedź: {output_path}")

    try:
        history = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Odpowiedź nie jest poprawnym JSON-em.")
        return 1

    if not isinstance(history, list):
        print("Nieoczekiwana struktura danych. Sprawdź zapisany plik.")
        return 1

    print(f"Region zapytania: {COUNTRY}")
    print(f"Żądany początek historii: {SINCE}")
    print(f"Liczba rekordów: {len(history)}")

    if not history:
        print("API nie zwróciło historii dla podanych parametrów.")
        return 0

    dates = []
    shops = set()
    currencies = set()
    incomplete_records = 0

    for record in history:
        try:
            # Zamieniamy datę tekstową na obiekt daty.
            date = datetime.fromisoformat(
                record["timestamp"].replace("Z", "+00:00")
            )

            if date.tzinfo is None:
                raise ValueError("Brak strefy czasowej")

            shop = record["shop"]["name"]
            currency = record["deal"]["price"]["currency"]

            if not isinstance(shop, str) or not isinstance(currency, str):
                raise ValueError("Niepoprawna nazwa sklepu lub waluta")

        except (KeyError, TypeError, ValueError, AttributeError):
            incomplete_records += 1
            continue

        dates.append(date.astimezone(timezone.utc))
        shops.add(shop)
        currencies.add(currency)

    if dates:
        print(f"Najstarszy odczytany wpis: {min(dates).isoformat()}")
        print(f"Najnowszy odczytany wpis: {max(dates).isoformat()}")
        print(f"Sklepy: {', '.join(sorted(shops))}")
        print(f"Waluty: {', '.join(sorted(currencies))}")

    print(f"Rekordy pominięte w podsumowaniu: {incomplete_records}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())