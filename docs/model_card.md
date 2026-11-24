# Model Card

## Model

- `ag_fast` — AutoGluon `WeightedEnsemble_L2`, wytrenowany lokalnie 23.11.2026.
- Artefakt W&B `production` — adres i wersja do uzupełnienia po publikacji.

## Przeznaczenie

- Wspiera decyzję technika o dodatkowej kontroli maszyny.
- Target — `Machine failure`. Klasa pozytywna `1` oznacza awarię.

## Dane

- `ai4i_2020`, podział stratyfikowany 80/20, `random_state=42`.
- Fingerprint przygotowanych danych — `317d6fd9e5bfa21b`.

## Metryki

- F1 **0,780**, precyzja **0,920**, recall **0,676**, accuracy **0,987**.
- Macierz pomyłek — TN 1928, FP 4, FN 22, TP 46.
- Dla porównania F1 regresji logistycznej wyniosło 0,177, a wcześniejszy
  wynik `DummyClassifier` wyniósł 0,000.

## Ograniczenia i ryzyka

- Dane są syntetyczne. Przed użyciem w zakładzie potrzebna jest walidacja
  na rzeczywistych danych. Model przeoczył 22 z 68 awarii na zbiorze testowym.

## Wersje

- Git SHA treningu — `28a05c25141ec0c7f47f0779758306b9cddd87d2`.
- AutoGluon Tabular 1.6.3, LightGBM 4.7.0, pandas 2.3.3, scikit-learn 1.7.2.
