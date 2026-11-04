import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from src import analyze_history


def make_record():
    """Tworzy nowy, poprawny rekord testowy."""
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "shop": {
            "id": 61,
            "name": "Steam",
        },
        "deal": {
            "price": {
                "amount": 10,
                "amountInt": 1000,
                "currency": "USD",
            },
            "regular": {
                "amount": 20,
                "amountInt": 2000,
                "currency": "USD",
            },
            "cut": 50,
        },
    }


class TestAnalyzeHistory(unittest.TestCase):
    def run_analysis(self, records):
        """Uruchamia analizator na tymczasowym pliku JSON."""
        with tempfile.TemporaryDirectory() as directory:
            test_path = Path(directory) / "test_history.json"
            test_path.write_text(
                json.dumps(records),
                encoding="utf-8",
            )

            output = io.StringIO()

            # Na czas testu podmieniamy ścieżkę do danych.
            with patch.object(analyze_history, "INPUT_PATH", test_path):
                with redirect_stdout(output):
                    exit_code = analyze_history.main()

            return exit_code, output.getvalue()

    def test_valid_record(self):
        exit_code, output = self.run_analysis([make_record()])

        self.assertEqual(exit_code, 0)
        self.assertIn("Rekordy odczytane poprawnie: 1", output)
        self.assertIn(
            "Rekordy z błędną strukturą lub wartościami: 0", output
        )
        self.assertIn("Identyczne duplikaty: 0", output)
        self.assertIn("Ujemne ceny ofert: 0", output)
        self.assertIn(
            "Rozbieżności amount × 100 i amountInt dla USD: 0", output
        )

    def test_duplicate_record(self):
        record = make_record()
        _, output = self.run_analysis([record, deepcopy(record)])

        self.assertIn("Identyczne duplikaty: 1", output)
        self.assertIn(
            "Powtórzenia klucza sklep + czas UTC + waluta: 1", output
        )

    def test_negative_price(self):
        record = make_record()
        record["deal"]["price"]["amount"] = -5
        record["deal"]["price"]["amountInt"] = -500

        _, output = self.run_analysis([record])

        self.assertIn("Ujemne ceny ofert: 1", output)
        self.assertIn(
            "Rozbieżności amount × 100 i amountInt dla USD: 0", output
        )

    def test_missing_price(self):
        record = make_record()
        del record["deal"]["price"]

        exit_code, output = self.run_analysis([record])

        self.assertEqual(exit_code, 1)
        self.assertIn("Rekordy odczytane poprawnie: 0", output)
        self.assertIn(
            "Rekordy z błędną strukturą lub wartościami: 1", output
        )

    def test_amount_int_mismatch(self):
        record = make_record()
        record["deal"]["price"]["amountInt"] = 999

        _, output = self.run_analysis([record])

        self.assertIn(
            "Rozbieżności amount × 100 i amountInt dla USD: 1", output
        )
        self.assertIn("Ujemne ceny ofert: 0", output)


if __name__ == "__main__":
    unittest.main()