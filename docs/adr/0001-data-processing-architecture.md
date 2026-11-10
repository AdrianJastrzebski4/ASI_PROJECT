# ADR-1: Architektura i podział logiki przetwarzania danych (Data Processing Architecture)

- **Status:** proponowany
- **Sprint:** S2
- **Autor:** Kamil Bertram
- **Recenzent:** imię i nazwisko (inna osoba niż autor)

## Kontekst

Przenosimy proces treningowy z notatnika do pipeline'u w Kedro. Naszym problemem jest odpowiednie ulokowanie logiki czyszczenia i transformacji danych. Musimy zagwarantować, że proces będzie wolny od wycieku danych (data leakage) podczas treningu, a jednocześnie kod czyszczący dane będzie mógł zostać bezpiecznie użyty w API do predykcji pojedynczych zapytań (gdzie nie mamy dostępu do targetu, ani pełnego zbioru). Naszym ograniczeniem jest narzucony kontrakt zbioru AI4I 2020.

## Rozważone opcje

1. Opcja A (Monolit) — Wszystkie operacje (czyszczenie, usuwanie braków, usuwanie duplikatów i skalowanie) zawarte w jednej wielkiej funkcji przygotowującej dane przed przekazaniem ich do modelu.
2. Opcja B (Trójwarstwowy podział) — Rozdzielenie logiki na 3 warstwy: normalizację wejścia (normalize_input), filtrowanie działające tylko przy treningu (filter_training_rows) oraz preprocessing wewnątrz modelu.

## Decyzja

Wybieramy Opcję B.

Dzięki temu podziałowi nasza funkcja normalize_input działa wyłącznie na pojedynczym rekordzie (np. usuwa białe znaki) i może trafić prosto do API. Funkcja filter_training_rows służy tylko do wyrzucania śmieci ze zbioru treningowego (np. duplikatów lub braków targetu), a cały preprocessing wymagający statystyk (metoda fit()) jest bezpiecznie chroniony przed wyciekiem wewnątrz Pipeline.

Decyzja opiera się na specyfice naszego zbioru, wymuszającej wysoką ostrożność przy podziale i transformacji:

| Wielkość                     | Wartość          | Skąd pochodzi                                |
|------------------------------|------------------|----------------------------------------------|
| Balans klas (Target)         | ~3.4% awarii     | Wyniki z notatnika EDA (Sprint 1)            |
| Liczba cech do przetworzenia | 6 (5 num, 1 kat) | Konfiguracja project.yaml (ALLOWED FEATURES) |
| Rozmiar zbioru testowego     | 0.2 (20%)        | Konfiguracja project.yaml (test_size)        |

## Odrzucone alternatywy

Odrzuciliśmy Opcję A (Monolit). Umieszczenie filtrowania wierszy (np. zrzucania duplikatów i rekordów bez targetu) w tym samym miejscu co skalowanie czy wdrożenie do API jest niedopuszczalne. Na produkcji system nie może odrzucić zapytania klienta tylko dlatego, że "jest duplikatem" lub "nie ma etykiety" (etykietę przecież dopiero próbujemy przewidzieć). Z kolei przeniesienie logiki fit() z scikit-learn do nodów Kedro przed splitem groziłoby krytycznym wyciekiem informacji ze zbioru testowego.

## Konsekwencje

Co ułatwia: Implementację API produkcyjnego w przyszłych sprintach. Aplikacja kliencka wywoła po prostu gotową funkcję normalize_input i przekaże dane do wczytanego modelu.

Co utrudnia: Wymaga od zespołu żelaznej dyscypliny podczas dodawania nowych reguł. Zabrania się używania jakichkolwiek funkcji wyliczających statystyki całego zbioru (np. średnich, median) w pliku data.py.

Co trzeba będzie zrobić: Przy integracji następnych Sprintów trzeba będzie pamiętać, by nowo dodawane zmienne wchodziły do właściwego miejsca (Kedro Node vs Sklearn Pipeline).

## Historia

| Data       | Zmiana |
|------------|---|
| 10.11.2026 | utworzenie |
