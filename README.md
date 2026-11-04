# Game Price ETL

Projekt portfolio z inżynierii danych, którego celem jest
zbudowanie procesu ETL do zbierania i analizowania historii
cen gier komputerowych.

Projekt rozwijam od podstaw przy wsparciu AI (ChatGPT).
Chcę pokazać zarówno rozumienie logiki ETL, jak i umiejętność
korzystania z AI podczas projektowania, pisania kodu,
rozwiązywania problemów i dokumentowania pracy.

## Cel projektu

Docelowo aplikacja będzie:
- pobierać ceny gier z zewnętrznego API;
- zapisywać surowe dane źródłowe;
- porządkować dane i sprawdzać ich poprawność;
- przechowywać historię cen w bazie danych;
- udostępniać dane do analiz i wizualizacji.

## Aktualny stan

Działa pierwszy etap pobierania danych z API IsThereAnyDeal:
- odczyt klucza API z konfiguracji;
- wyszukiwanie gier po nazwie;
- pobieranie historii cen wybranej gry i regionu;
- zapis odpowiedzi API do plików JSON;
- podstawowe podsumowanie zakresu dat, sklepów i walut.

Dla Hollow Knight wykonano zapytania dla dwóch regionów:
- PL: 20 rekordów, waluty EUR i PLN;
- US: 398 rekordów, waluta USD.

Są to wyniki pierwszego testu, a nie stałe wielkości zbioru.
Kompletność i jakość historii wymagają dalszej weryfikacji.

Kolejny etap to analiza zapisanych danych: zakres historii
poszczególnych sklepów, brakujące wartości oraz duplikaty.
Baza danych, transformacje i harmonogram nie są jeszcze wdrożone.

## Technologie

Na początkowym etapie:
- Python;
- PyCharm;
- Git;
- requests — obsługa zapytań HTTP;
- python-dotenv — odczyt lokalnej konfiguracji.

W dalszych etapach planowane jest wykorzystanie PostgreSQL
oraz SQL do przechowywania i przekształcania danych.

## Struktura projektu

- src/ — kod aplikacji;
- docs/ — dokumentacja projektu;
- data/ — lokalnie przechowywane dane, pomijane przez Git;
- .env.example — wzór konfiguracji bez klucza API;
- requirements.txt — lista zależności.

## Współpraca z AI

AI wspiera planowanie, proponowanie kodu, wyjaśnianie
rozwiązań oraz przygotowywanie dokumentacji.

Moją rolą jest rozumienie proponowanych rozwiązań,
podejmowanie decyzji i sprawdzanie działania kodu.
W dokumentacji rozróżniam funkcje planowane od wykonanych
oraz wyników faktycznie zweryfikowanych.

Ważniejsze przykłady współpracy i weryfikacji zapisuję
w [dokumentacji współpracy z AI](docs/ai_collaboration.md).