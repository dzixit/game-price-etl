# Współpraca z AI

W tym dokumencie zapisuję istotne przykłady wykorzystania
ChatGPT podczas realizacji projektu: propozycje, podjęte
decyzje i sposób sprawdzania rozwiązań.

Nie jest to pełny zapis rozmów. Dokument ma pokazywać,
jak wykorzystuję AI i jak oceniam jego podpowiedzi.

## 1. Wybór początkowego podejścia

### Zadanie
Wybrać sposób rozpoczęcia projektu ETL dotyczącego cen gier.
Rozważałem zwykły projekt Pythona oraz wykorzystanie PySparka.

### Wsparcie AI
AI zaproponowało rozpoczęcie od projektu Pure Python,
pobierania danych przez API i zapisywania odpowiedzi do JSON.
PySpark został wskazany jako możliwe późniejsze rozszerzenie.

### Podjęta decyzja
Rozpocząłem od projektu Pure Python w PyCharmie.
Na pierwszym etapie skupiam się na poznaniu danych
i zbudowaniu działającego procesu pobierania.

Nie mam jeszcze wyników pomiarów, które uzasadniałyby
zastosowanie przetwarzania rozproszonego.

### Wykonane działania
- Utworzyłem projekt w PyCharmie.
- Utworzyłem foldery src, docs i data.
- Przygotowałem plik .gitignore na podstawie propozycji AI.

### Stan weryfikacji
Struktura projektu została przygotowana.
Dostęp do API i zakres dostępnej historii cen nie zostały
jeszcze zweryfikowane.

### Kolejny krok
Przygotować konfigurację, wykonać pierwsze zapytanie do API
i udokumentować rzeczywisty wynik.