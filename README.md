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

Projekt jest na etapie przygotowania środowiska
i sprawdzania możliwości pozyskania danych.

Utworzono strukturę folderów oraz plik .gitignore.
Kolejnym krokiem jest przygotowanie konfiguracji API
i uruchomienie pierwszego zapytania.

Dostępność wieloletniej historii cen dla wybranego rynku
wymaga weryfikacji.

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