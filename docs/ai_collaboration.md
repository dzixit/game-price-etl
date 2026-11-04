# Współpraca z AI

Projekt tworzę przy wsparciu ChatGPT. Wykorzystuję AI
do planowania pracy, przygotowywania kodu, wyjaśniania
rozwiązań i analizy problemów.

W tym dokumencie zapisuję ważniejsze przykłady współpracy:
co zaproponowało AI, jakie decyzje podjąłem oraz jak
sprawdziłem wyniki. Szczegółowy przebieg uruchomień znajduje
się w [dzienniku prac](development_log.md).

## 1. Wybór początkowego podejścia

### Zadanie
Wybrać sposób rozpoczęcia projektu ETL dotyczącego cen gier.
Rozważałem zwykły projekt Pythona oraz wykorzystanie PySparka.

### Wsparcie AI
AI zaproponowało rozpoczęcie od Pythona, pobierania danych
przez API i zapisywania odpowiedzi do JSON.
PySpark został wskazany jako możliwe późniejsze rozszerzenie.

### Moja decyzja i działania
Rozpocząłem od projektu Pure Python w PyCharmie.
Utworzyłem środowisko wirtualne, strukturę folderów
i pliki konfiguracyjne.

Na tym etapie priorytetem jest poznanie źródła danych
i zbudowanie działającego procesu pobierania.
Nie mam wyników pomiarów uzasadniających użycie Sparka.

### Weryfikacja
Uruchomiłem skrypt sprawdzający konfigurację.
Najpierw otrzymałem komunikat o braku klucza, a po jego
uzupełnieniu potwierdziłem poprawny odczyt konfiguracji.

## 2. Pierwsze pobranie danych i wybór gry

### Zadanie
Połączyć się z IsThereAnyDeal i znaleźć identyfikator
podstawowej gry Hollow Knight.

### Wsparcie AI
AI przygotowało kod wysyłający zapytanie do API,
obsługujący błędy i zapisujący odpowiedź do pliku JSON.
Wyjaśniło też rolę identyfikatora gry.

### Moje działania i weryfikacja
Uruchomiłem skrypt lokalnie. API zwróciło status HTTP 200
i pięć wyników wyszukiwania.

Sprawdziłem zwrócone tytuły. Oprócz podstawowej gry
wyniki obejmowały Silksong i ścieżki dźwiękowe.
Do dalszego testu wybrałem rekord Hollow Knight:

018d937f-1ae9-734c-ba47-bd357cf07edd

### Wniosek
Samo podobieństwo nazw nie wystarcza do utożsamienia
produktów. Dalsze zapytania wykonuję z użyciem
identyfikatora wybranego rekordu.

## 3. Porównanie historii dla PL i US

### Zadanie
Sprawdzić, czy źródło udostępnia dane pozwalające
analizować ceny na przestrzeni lat.

### Wsparcie AI
AI przygotowało skrypt pobierający historię cen.
Po uzyskaniu krótkiej historii dla Polski zaproponowało
wykonanie analogicznego zapytania dla USA.

### Moje działania i weryfikacja
Uruchomiłem zapytania dla tej samej gry i tego samego
początku okresu: 2017-01-01.

- PL: 20 rekordów z 2026 roku, waluty EUR i PLN.
- US: 398 rekordów z datami od 2017 do 2026 roku,
  waluta USD.

Zachowałem osobne pliki źródłowe dla obu regionów.

### Podjęta decyzja
Do kolejnego etapu analizy wykorzystuję próbkę US,
ponieważ zawiera dłuższą historię dla badanej gry.
Nie traktuję jej jako uzupełnienia polskich cen.

### Ograniczenia
Test dotyczy jednej gry. Nie potwierdza pokrycia
całego katalogu ani kompletności historii.
Przyczyna krótszego zakresu danych PL pozostaje nieustalona.

## 4. Analiza JSON i lokalne odtworzenie wyników

### Zadanie
Sprawdzić strukturę danych, duplikaty, ceny i zakres
historii poszczególnych sklepów.

### Wsparcie AI
Przekazałem zapisany plik US do analizy w ChatGPT.
AI przeanalizowało dane, a następnie przygotowało
analyze_history.py do wykonania kontroli lokalnie.

### Moje działania
Uruchomiłem skrypt w PyCharmie na tym samym pliku
i porównałem wynik z wcześniejszą analizą AI.

### Wynik weryfikacji
- Odczytano poprawnie 398 z 398 rekordów.
- Nie wykryto identycznych duplikatów.
- Nie wykryto powtórzeń klucza sklep + czas UTC + waluta.
- Nie wykryto ujemnych cen ofert.
- Nie wykryto cen ofert wyższych od cen regularnych.
- Dla USD nie wykryto różnic między amount × 100 a amountInt.
- Zakres cen wyniósł 5,09–17,21 USD.
- Skrypt zakończył się kodem 0.

Wyniki tych kontroli były zgodne z wcześniejszą analizą.
Lokalny skrypt przedstawia daty w UTC, co może zmienić
dzień kalendarzowy względem zapisu ze strefą źródłową.

### Wnioski i ograniczenia
Najwięcej rekordów mają GOG, Humble Store i Steam.
Zakres historii trzeba oceniać osobno dla każdego sklepu.

Wpis Humble Widgets z ceną 15 USD ma czas równy
początkowi zapytania. Jego znaczenie pozostaje
niewyjaśnione i wymaga dalszej weryfikacji.

Uruchomienie skryptu pozwoliło odtworzyć analizę lokalnie.
Nie stanowi jednak niezależnego dowodu poprawności
wszystkich reguł, ponieważ kod również przygotowano
przy wsparciu AI. Następnie wykonano pięć testów na przygotowanych danych,
w tym przypadkach z celowo wprowadzonymi błędami.
Ich przebieg opisano w sekcji 6.

## 5. Uwagi z przeglądu kodu

Podczas przeglądu AI wskazało ograniczenia wcześniejszych
propozycji kodu:

- check_config.py przy braku klucza kończy się kodem 0;
- fetch_history.py może zwrócić kod 0 również wtedy,
  gdy wszystkie rekordy zostaną pominięte w podsumowaniu.

Na podstawie przeglądu poprawiono oba zachowania.
AI zaproponowało zmiany i testy, które dodałem oraz
uruchomiłem lokalnie.

Cztery testy konfiguracji i cztery testy pobierania historii
zakończyły się powodzeniem. Łącznie z wcześniejszymi
testami analizatora zaliczono 13 testów.

Sprawdzono również zachowanie surowej odpowiedzi przy
niepoprawnych rekordach. Testy nie wymagały połączenia z API.

## 6. Testowanie na celowo błędnych danych

### Wsparcie AI
AI przygotowało testy unittest oraz wyjaśniło wykorzystanie
plików tymczasowych i podmiany ścieżki wejściowej.

### Moje działania i weryfikacja
Dodałem testy do projektu i uruchomiłem je lokalnie.
Wszystkie pięć przypadków zakończyło się powodzeniem.

Testy potwierdziły wykrywanie przygotowanych błędów.
Ponieważ analizator i testy powstały przy wsparciu AI,
wynik traktuję jako sprawdzenie konkretnych zachowań,
a nie pełne potwierdzenie poprawności programu.

## Następne działania

- Poprawić sygnalizowanie błędów w skryptach.
- Wyjaśnić znaczenie najstarszego wpisu historii.