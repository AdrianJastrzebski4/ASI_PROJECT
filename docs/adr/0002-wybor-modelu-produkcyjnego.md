# ADR-2: Wybór modelu produkcyjnego

- **Status** — zaakceptowany
- **Sprint** — S3
- **Autor** — Adrian Jastrzębski
- **Recenzent** — Antoni Kluczkowski

## Kontekst

Wybieramy model do klasyfikacji awarii maszyn na danych `ai4i_2020`.
W Sprincie 4 API ma wczytywać gotowy pakiet modelu bez uruchamiania treningu.
Porównaliśmy trzy modele na tym samym zbiorze testowym, uwzględniając F1
dla klasy awarii, czas predykcji, rozmiar modelu i pamięć po wczytaniu.

## Rozważone opcje

1. `baseline` — regresja logistyczna z pipeline'u Kedro ze Sprintu 2.
2. `ag_fast` — AutoGluon z presetem `medium_quality` i limitem 30 s.
3. `ag_good` — AutoGluon z presetem `good_quality` i limitem 90 s.

## Decyzja

Wybieramy `ag_fast`, w którym AutoGluon wskazał `WeightedEnsemble_L2`
jako najlepszy model. Decyzję opieramy na lokalnym benchmarku z 23.11.2026,
wykonanym po treningu na pełnych danych.

| Model | F1 | Predykcja całego zbioru testowego [ms] | Rozmiar zapisanego modelu [MiB] | Przyrost pamięci przy wczytaniu [MiB] |
|---|---:|---:|---:|---:|
| `baseline` | 0,177 | 2,912 | 0,003 | 0,043 |
| `ag_fast` | 0,780 | 64,324 | 35,846 | 11,852 |
| `ag_good` | 0,820 | 460,938 | 108,817 | 1,039 |

`ag_fast` wykonał predykcję całego zbioru testowego około 7 razy szybciej
niż `ag_good` i zajmował około 3 razy mniej miejsca na dysku.
Akceptujemy niższe F1 o 0,040. Na zbiorze testowym `ag_fast` wykrył 46 z 68
awarii, a `ag_good` wykrył 50. Pomiar pamięci pochodzi z jednego przebiegu
we wspólnym procesie i ma charakter orientacyjny.

Pakiet zawiera katalog `model/` i plik `metadata.json`.

- Artefakt W&B — `s31194-polish-japanese-academy-of-information-technology/asi-project/ag-fast:v0`, alias `production`.
- Smoke test (24.11.2026) — pobranie i wczytanie pakietu w osobnym procesie zakończone sukcesem. Model zwrócił pięć etykiet `[0, 0, 0, 0, 0]`.

## Odrzucone alternatywy

- `baseline` — odrzuciliśmy go ze względu na znacznie niższe F1 (0,177)
  mimo krótkiego czasu predykcji i małego rozmiaru.
- `ag_good` — uzyskał najwyższe F1 (0,820), ale predykcja całego zbioru
  trwała około 461 ms, a zapisany model zajmował około 109 MiB.
  Wybraliśmy szybszy i mniejszy wariant.

## Konsekwencje

API w Sprincie 4 będzie mogło użyć wspólnej funkcji ładowania pakietu.
Po publikacji smoke test w osobnym procesie pobierze artefakt `production`,
wczyta model i sprawdzi schemat predykcji dla pięciu wierszy.

## Historia

| Data       | Zmiana                                  |
|------------|-----------------------------------------|
| 2026-11-18 | Utworzenie szkicu                       |
| 2026-11-24 | Wybór `ag_fast` na podstawie benchmarku |
| 2026-11-25 | Recenzja                                |
