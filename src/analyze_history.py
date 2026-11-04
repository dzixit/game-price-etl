import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / (
    "history_018d937f-1ae9-734c-ba47-bd357cf07edd"
    "_US_20261104T202606533724Z.json"
)


def main():
    # Odczytujemy konkretny plik, aby analizę dało się powtórzyć.
    try:
        with INPUT_PATH.open(encoding="utf-8") as file:
            history = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Nie udało się odczytać pliku: {error}")
        return 1

    if not isinstance(history, list) or not history:
        print("Plik powinien zawierać niepustą listę rekordów.")
        return 1

    # Sortowanie kluczy pozwala porównywać treść rekordów,
    # niezależnie od kolejności pól w JSON-ie.
    serialized = [
        json.dumps(record, sort_keys=True)
        for record in history
    ]
    exact_duplicates = len(serialized) - len(set(serialized))

    shops = defaultdict(list)
    prices_by_currency = defaultdict(list)
    record_keys = Counter()

    negative_prices = 0
    prices_above_regular = 0
    amount_mismatches = 0
    invalid_records = []
    valid_records = []

    for index, record in enumerate(history, start=1):
        try:
            shop_id = record["shop"]["id"]
            shop_name = record["shop"]["name"]

            if type(shop_id) is not int:
                raise ValueError("ID sklepu nie jest liczbą całkowitą")

            if not isinstance(shop_name, str) or not shop_name.strip():
                raise ValueError("Brak poprawnej nazwy sklepu")

            timestamp = datetime.fromisoformat(
                record["timestamp"].replace("Z", "+00:00")
            )

            if timestamp.tzinfo is None:
                raise ValueError("Data nie zawiera strefy czasowej")

            timestamp = timestamp.astimezone(timezone.utc)

            price_data = record["deal"]["price"]
            regular_data = record["deal"]["regular"]

            currency = price_data["currency"]

            if not isinstance(currency, str) or not currency.strip():
                raise ValueError("Brak poprawnej waluty")

            if regular_data["currency"] != currency:
                raise ValueError("Cena oferty i regularna mają różne waluty")

            # Decimal pozwala wykonywać dokładne obliczenia dziesiętne.
            price = Decimal(str(price_data["amount"]))
            regular = Decimal(str(regular_data["amount"]))
            amount_int = price_data["amountInt"]

            if not price.is_finite() or not regular.is_finite():
                raise ValueError("Cena nie jest skończoną liczbą")

            if type(amount_int) is not int:
                raise ValueError("amountInt nie jest liczbą całkowitą")

        except (KeyError, TypeError, ValueError, AttributeError,
                ArithmeticError) as error:
            invalid_records.append((index, str(error)))
            continue

        negative_prices += int(price < 0)
        prices_above_regular += int(price > regular)

        # W tej analizie sprawdzamy relację amountInt dla USD.
        if currency == "USD":
            amount_mismatches += int(price * 100 != amount_int)

        record_keys[(shop_id, timestamp, currency)] += 1
        shops[(shop_id, shop_name)].append(timestamp)
        prices_by_currency[currency].append(price)

        valid_records.append({
            "timestamp": timestamp,
            "shop": shop_name,
            "price": price,
            "currency": currency,
        })

    key_duplicates = sum(count - 1 for count in record_keys.values())

    print(f"Plik: {INPUT_PATH.name}")
    print(f"Liczba wszystkich rekordów: {len(history)}")
    print(f"Rekordy odczytane poprawnie: {len(valid_records)}")
    print(f"Rekordy z błędną strukturą lub wartościami: {len(invalid_records)}")
    print(f"Identyczne duplikaty: {exact_duplicates}")

    print("\nKontrole dla poprawnie odczytanych rekordów:")
    print(f"Powtórzenia klucza sklep + czas UTC + waluta: {key_duplicates}")
    print(f"Ujemne ceny ofert: {negative_prices}")
    print(f"Ceny ofert wyższe od regularnych: {prices_above_regular}")
    print(f"Rozbieżności amount × 100 i amountInt dla USD: {amount_mismatches}")

    print("\nZakres cen według waluty:")
    for currency, prices in sorted(prices_by_currency.items()):
        print(f"{currency}: {min(prices):.2f}–{max(prices):.2f}")

    print("\nHistoria sklepów — daty w UTC:")
    for (shop_id, shop_name), dates in sorted(shops.items()):
        print(
            f"{shop_name} (ID: {shop_id}): {len(dates)} rekordów | "
            f"{min(dates).date()} — {max(dates).date()}"
        )

    print("\nPięć najstarszych poprawnie odczytanych rekordów:")
    oldest = sorted(valid_records, key=lambda row: row["timestamp"])[:5]

    for row in oldest:
        print(
            f"{row['timestamp'].isoformat()} | {row['shop']} | "
            f"{row['price']:.2f} {row['currency']}"
        )

    if invalid_records:
        print("\nRekordy wymagające sprawdzenia (numeracja od 1):")
        for index, reason in invalid_records:
            print(f"Rekord {index}: {reason}")

    print("\nAnaliza nie potwierdza kompletności historii.")

    # Sygnalizujemy błąd, jeżeli nie udało się odczytać części rekordów.
    return 1 if invalid_records else 0


if __name__ == "__main__":
    raise SystemExit(main())