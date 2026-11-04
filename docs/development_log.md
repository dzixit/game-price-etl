# Dziennik prac

## Etap 1 — przygotowanie projektu

### Wykonane prace
- Utworzono projekt Python z osobnym środowiskiem wirtualnym.
- Utworzono foldery src, docs i data.
- Dodano reguły .gitignore.
- Dodano zależności requests i python-dotenv.
- Przygotowano skrypt sprawdzający obecność klucza API.

### Weryfikacja
- Uruchomiono src/check_config.py.
- Wynik: Brak klucza API. Uzupełnij ITAD_API_KEY w pliku .env.

### Kolejny krok
Uzyskanie klucza API i wykonanie pierwszego zapytania.

## Pierwsze zapytanie do API

### Wykonane działania
- Potwierdzono odczyt klucza przez check_config.py.
- Dodano search_game.py do wyszukiwania gry Hollow Knight.
- Zapisano odpowiedź API w data/raw.

### Wynik weryfikacji
- Status HTTP: 200.
- Skrypt zakończył się bez błędu (exit code 0).
- API zwróciło 5 wyników: podstawową grę Hollow Knight,
  Hollow Knight: Silksong oraz trzy pozycje związane
  ze ścieżkami dźwiękowymi.

### Wniosek
Wyszukiwanie po nazwie zwraca również powiązane produkty.
Nie należy automatycznie traktować wszystkich wyników
jako tej samej gry ani zakładać, że pierwszy wynik
zawsze będzie właściwy.

### Podjęta decyzja
Do pierwszego testu pobierania historii cen wybrano ręcznie
rekord o tytule Hollow Knight.

- ID: 018d937f-1ae9-734c-ba47-bd357cf07edd.

W kolejnych zapytaniach dotyczących tej gry wykorzystamy
jej identyfikator w IsThereAnyDeal.

### Kolejny krok
Pobrać historię cen wybranej gry dla regionu PL
i sprawdzić zakres dostępnych danych.

## Pobranie historii cen — region PL

- Wybrano podstawową grę Hollow Knight.
- ID gry: 018d937f-1ae9-734c-ba47-bd357cf07edd.
- Region zapytania: PL.
- Żądany początek historii: 2017-01-01.
- Status HTTP: 200.
- Liczba rekordów: 20.
- Najstarszy odczytany wpis: 2026-01-29T20:21:51+00:00.
- Najnowszy odczytany wpis: 2026-09-03T17:06:56+00:00.
- Sklepy: GOG, GreenManGaming, Humble Store, Steam
- Zwrócone waluty: EUR, PLN.
- Rekordy pominięte w podsumowaniu: 0.
- Kompletność historii: jeszcze niezweryfikowana.

### Wnioski
Zapytanie obejmowało okres od 2017-01-01, ale otrzymana
odpowiedź zawiera jedynie 20 rekordów z 2026 roku.
Przyczyna ograniczonego zakresu nie została jeszcze ustalona.

Dla regionu PL zwrócono ceny w EUR i PLN.
W analizach należy zachować informację o walucie
i nie porównywać bezpośrednio kwot w różnych walutach.

Brak rekordów pominiętych w podsumowaniu oznacza, że wszystkie
rekordy zawierały pola odczytywane przez skrypt.
Nie potwierdza to kompletności ani pełnej poprawności danych.

### Kolejny krok
Wykonać analogiczne zapytanie dla regionu US i porównać
liczbę rekordów, zakres dat, sklepy oraz waluty.

## Pobranie historii cen — region US

### Cel
Sprawdzić, czy dla tej samej gry region US udostępnia
dłuższą historię cen niż region PL.

### Wykonane działania
- Zmieniono COUNTRY z PL na US w fetch_history.py.
- Zachowano identyfikator gry Hollow Knight:
  018d937f-1ae9-734c-ba47-bd357cf07edd.
- Zachowano początek zapytania: 2017-01-01T00:00:00Z.
- Uruchomiono skrypt i zapisano osobną odpowiedź w data/raw.
- Zachowano wcześniej pobrany plik dla regionu PL.

### Wynik weryfikacji
- Status HTTP: 200.
- Skrypt zakończył się bez błędu (exit code 0).
- Liczba rekordów: 398.
- Najstarszy odczytany wpis: 2017-01-01T00:00:00+00:00.
- Najnowszy odczytany wpis: 2026-09-03T17:06:56+00:00.
- Sklepy: Discord Store, Fanatical, GOG, GreenManGaming,
  Humble Store, Humble Widgets, IndieGala Store,
  Microsoft Store, Steam.
- Zwrócona waluta: USD.
- Rekordy pominięte w podsumowaniu: 0.
- Kompletność historii: jeszcze niezweryfikowana.

### Porównanie regionów

| Cecha | PL | US |
|---|---|---|
| Liczba rekordów | 20 | 398 |
| Najstarszy odczytany wpis | 2026-01-29 | 2017-01-01 |
| Najnowszy odczytany wpis | 2026-09-03 | 2026-09-03 |
| Liczba sklepów | 4 | 9 |
| Waluty | EUR, PLN | USD |

### Wnioski
Dla przetestowanej gry odpowiedź dla regionu US zawiera
więcej rekordów i obejmuje dłuższy okres niż odpowiedź
dla regionu PL. Region US jest więc kandydatem do dalszych
testów analizy wieloletniej historii cen.

Wynik dotyczy jednej gry. Nie potwierdza analogicznego
pokrycia dla całego planowanego katalogu.

Skrajne daty nie potwierdzają ciągłości ani kompletności
historii. Zakres danych należy sprawdzić osobno dla sklepów.

Najstarszy wpis ma datę identyczną z początkiem zapytania.
Przed uznaniem go za rzeczywistą zmianę ceny trzeba sprawdzić
jego zawartość i sposób wyznaczania dat przez źródło.

Dane dla PL i US dotyczą różnych rynków. Historia US
nie stanowi uzupełnienia brakujących polskich cen.

### Kolejny krok
Przeanalizować zapisany plik JSON dla US bez ponownego
pobierania danych. Sprawdzić najstarsze rekordy, zakres
dat dla poszczególnych sklepów, braki i duplikaty.

## Analiza pliku historii US przy wsparciu AI

### Wykonane działania
Przekazano zapisany plik JSON do analizy w ChatGPT.
Sprawdzenia wykonano na pliku, bez ponownego pobierania danych.

### Wyniki
- Liczba rekordów: 398.
- Identyczne duplikaty: 0.
- Powtórzenia kombinacji sklep ID + znacznik czasu + waluta: 0.
- Wszystkie ceny ofert są w USD.
- Zakres cen ofert: 5,09–17,21 USD.
- Ujemne ceny ofert: 0.
- Ceny ofert wyższe od cen regularnych: 0.
- Rozbieżności między amount × 100 a amountInt: 0.

Najwięcej rekordów mają GOG (126), Humble Store (117)
i Steam (115). Każdy z tych sklepów ma wpisy z lat 2017–2026,
ale ciągłość historii pozostaje niepotwierdzona.

Najstarszy wpis należy do Humble Widgets i ma cenę 15 USD.
Jest jedynym rekordem tego sklepu, a jego czas odpowiada
dokładnie początkowi zapytania. Znaczenie tej daty wymaga
dalszego sprawdzenia.

### Wnioski
Zakres historii należy oceniać osobno dla każdego sklepu.
Pojedynczego wpisu nie można traktować jako dowodu stałej
ceny w całym analizowanym okresie.

### Kolejny krok
Przygotować lokalny skrypt analizy JSON i odtworzyć wyniki
w PyCharmie, aby weryfikacja była powtarzalna.

## Lokalna weryfikacja analizy historii US

### Wykonane działania
- Dodano src/analyze_history.py.
- Uruchomiono analizę na wcześniej zapisanym pliku US.
- Nie wykonywano nowych zapytań do API.
- Porównano wynik lokalny z wcześniejszą analizą ChatGPT.

### Wynik
- Poprawnie odczytano 398 z 398 rekordów.
- Nie wykryto identycznych duplikatów ani powtórzeń
  kombinacji sklep + czas UTC + waluta.
- Nie wykryto ujemnych cen, cen ofert wyższych od regularnych
  ani rozbieżności amount × 100 i amountInt dla USD.
- Zakres cen: 5,09–17,21 USD.
- Skrypt zakończył się kodem 0.
- Wyniki sprawdzonych kontroli były zgodne z analizą AI.

### Ograniczenia
Sprawdzenia dotyczą jednego pliku i określonych reguł.
Nie potwierdzają kompletności historii.
Analizator nie został jeszcze przetestowany na danych
z celowo wprowadzonymi błędami.

### Kolejny krok
Sprawdzić wykrywanie błędów na małych danych testowych.

## Testy analizatora na celowo błędnych danych

### Wykonane działania
- Dodano tests/test_analyze_history.py.
- Przygotowano pięć testów automatycznych w unittest.
- Testy korzystają z tymczasowych plików JSON.
- Oryginalne dane z API pozostają bez zmian.

### Sprawdzone przypadki
- Poprawny rekord.
- Dwa identyczne rekordy.
- Ujemna cena oferty.
- Brak pola price.
- Rozbieżność między amount a amountInt.

### Weryfikacja
Uruchomiono:
python -m unittest discover -s tests -v

Wynik: 5 testów zakończonych powodzeniem (OK).

### Wnioski
Analizator wykrywa problemy w przygotowanych przypadkach.
Obecnie duplikaty i nieprawidłowe ceny są raportowane,
ale nie powodują zwrócenia kodu błędu.
Brak wymaganego pola powoduje zwrócenie kodu 1.

### Kolejny krok
Poprawić sygnalizowanie błędów w check_config.py
i fetch_history.py oraz sprawdzić te zachowania testami.