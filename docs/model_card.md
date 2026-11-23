# Model Card

## Model

- Typ modelu i jego wersja — do uzupełnienia po wyborze modelu i publikacji artefaktu w W&B pod aliasem `production`.
- Data utworzenia i autor runu — do uzupełnienia na podstawie runu wybranego modelu w W&B.

## Przeznaczenie

- Problem — klasyfikacja binarna awarii maszyny. Target to `Machine failure`, a klasa pozytywna to `1` (awaria).
- Użytkownik systemu i wspierana decyzja — pracownik utrzymania ruchu może użyć wyniku jako wskazówki, czy skierować maszynę do dodatkowej kontroli.
- Zastosowania, do których model nie jest przeznaczony — automatyczne wyłączanie maszyn i samodzielne podejmowanie decyzji dotyczących bezpieczeństwa.

## Dane

- Dataset — `ai4i_2020` (AI4I 2020 Predictive Maintenance Dataset). Fingerprint SHA-256 do uzupełnienia z metadanych wybranego modelu.
- Strategia splitu — losowy podział stratyfikowany, 80% trening i 20% test, `random_state: 42`. Liczebności do potwierdzenia na podstawie wybranego runu.

## Metryki

- Metryka główna — F1 na zbiorze testowym. Wynik wybranego modelu i wynik `DummyClassifier` do uzupełnienia po ewaluacji.
- Pozostałe metryki i macierz pomyłek — do uzupełnienia wynikami wybranego modelu.

## Ograniczenia i ryzyka

- Ograniczenia danych — AI4I 2020 to zbiór syntetyczny. Przed użyciem w zakładzie trzeba zweryfikować model na rzeczywistych danych.
- Znane błędy i sytuacje, w których model zawodzi — do uzupełnienia po analizie błędów. Fałszywy alarm może prowadzić do zbędnej kontroli, a przeoczona awaria może opóźnić interwencję.

## Wersje

- Wersje bibliotek modelu i Git SHA treningu — do uzupełnienia z `metadata.json` wybranego pakietu.
