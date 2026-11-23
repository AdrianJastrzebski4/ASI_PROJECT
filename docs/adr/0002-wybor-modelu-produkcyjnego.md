# ADR-2: Wybór modelu produkcyjnego

- **Status:** proponowany
- **Sprint:** S3
- **Autor:** Adrian Jastrzębski
- **Recenzent:** do uzupełnienia po review

## Kontekst

Wybieramy model do klasyfikacji awarii maszyn na danych `ai4i_2020`.
W Sprincie 4 API ma pobierać i wczytywać gotowy pakiet modelu bez
uruchamiania treningu.

## Rozważone opcje

1. Regresja logistyczna z pipeline'u Kedro jako baseline ze Sprintu 2.
2. Pierwsza konfiguracja AutoGluona z limitem czasu treningu.
3. Druga konfiguracja AutoGluona z limitem czasu treningu.

## Decyzja

Do podjęcia po porównaniu modeli na tym samym zbiorze testowym.
Uwzględnimy F1 dla klasy awarii, czas predykcji, rozmiar pakietu
i zużycie pamięci po wczytaniu modelu.

| Wielkość | Wartość | Skąd pochodzi |
|---|---|---|
| F1 na zbiorze testowym | Do uzupełnienia | Runy W&B |
| Czas predykcji | Do uzupełnienia | Benchmark |
| Rozmiar pakietu | Do uzupełnienia | Benchmark |
| Pamięć po wczytaniu | Do uzupełnienia | Benchmark |

Wybrany pakiet będzie zawierał model i `metadata.json`. Opublikujemy go
jako W&B Artifact z aliasem `production`. Po publikacji wpiszemy tutaj
adres i konkretną wersję artefaktu.

## Odrzucone alternatywy

Po wyborze modelu opiszemy, które warianty odrzuciliśmy i jakie wyniki
uzasadniają tę decyzję.

## Konsekwencje

API w Sprincie 4 będzie mogło użyć wspólnej funkcji ładowania pakietu.
Po publikacji smoke test sprawdzi pobranie artefaktu `production`,
wczytanie modelu i schemat predykcji dla pięciu wierszy w osobnym procesie.

## Historia

| Data | Zmiana |
|---|---|
| 2026-11-18 | Utworzenie szkicu |
