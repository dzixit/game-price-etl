import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import check_config


class TestCheckConfig(unittest.TestCase):
    def run_check(self, environment):
        output = io.StringIO()

        # Nie odczytujemy prawdziwego pliku .env podczas testów.
        with patch.object(check_config, "load_dotenv"):
            # Tymczasowo zastępujemy zmienne środowiskowe.
            with patch.dict(os.environ, environment, clear=True):
                with redirect_stdout(output):
                    return check_config.main()

    def test_missing_key(self):
        self.assertEqual(self.run_check({}), 1)

    def test_empty_key(self):
        self.assertEqual(self.run_check({"ITAD_API_KEY": ""}), 1)

    def test_whitespace_key(self):
        self.assertEqual(self.run_check({"ITAD_API_KEY": "   "}), 1)

    def test_present_key(self):
        self.assertEqual(
            self.run_check({"ITAD_API_KEY": "test-placeholder"}),
            0,
        )


if __name__ == "__main__":
    unittest.main()