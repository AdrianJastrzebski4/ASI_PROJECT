# Architektura systemu

Ten dokument opisuje architekturę systemu zespołu. W Sprincie 1 powstaje diagram v0, który
będzie aktualizowany w kolejnych sprintach.

## Architektura docelowa (scaffold)

Tak wygląda system po sześciu sprintach — na poziomie warstw. To mapa odpowiedzialności,
a nie diagram do skopiowania: diagram v0 (niżej) rysujecie sami.

Relacje między warstwami (opis tekstowy, nie diagram):

- training: dane → pipeline Kedro → artefakt modelu
- serving: UI → API → model (artefakt wczytany przez API)
- state: API → persistence
- deployment: API + UI → Cloud Run

| Warstwa | Odpowiedzialność | Sprint | Miejsce w repozytorium |
|---|---|---|---|
| Dane i kontrakt | źródło danych, kontrakt, input normalization, training-only filtering | S1 | `data/01_raw/`, `src/asi_project/datasets.yaml`, `src/asi_project/data.py` |
| Pipeline | odtwarzalne przetwarzanie i trening od surowych danych | S2 | `conf/`, `src/asi_project/pipelines/` |
| Eksperymenty i artefakt | porównanie runów, wybór modelu, pakiet modelu ładowalny poza treningiem | S3 | W&B, pakiet modelu, `docs/model_card.md` |
| API | kontrakt usługi, walidacja na granicy, model wczytywany raz | S4 | `src/asi_project/api/`, `docker/` |
| Persistence | zapis predykcji poza procesem aplikacji (tryby `sql` / `disabled`) | S4 → S5 → S6 | repository w API, Postgres w compose |
| UI | formularz jako klient API | S5 | `ui/`, `docker/`, `docker-compose.yml` |
| Chmura | wdrożenie, sekret, logi, release | S6 | `deploy/`, Cloud Run, Secret Manager, Cloud Logging |

## Diagram v0 (Sprint 1)

Narysujcie, jak — według waszej obecnej wiedzy — będzie wyglądał system na koniec projektu.
Diagram v0 nie musi być poprawny w szczegółach; ma pokazać wasze rozumienie przepływu.
Sama lista warstw z sekcji wyżej nie wystarcza — diagram pokazuje wasz system i wasze decyzje.

Na diagramie zaznaczcie co najmniej:

- skąd pochodzą dane i gdzie żyje kontrakt danych;
- gdzie działa każdy z trzech typów przetwarzania: input normalization, training-only
  filtering, model preprocessing;
- gdzie powstaje model i jak trafia tam, gdzie wykonuje się predykcja;
- kto lub co wysyła żądanie predykcji i co dostaje w odpowiedzi;
- gdzie przechowywany jest stan (np. zapis predykcji);
- które elementy już istnieją po Sprincie 1, a które są planowane.

Diagram umieśćcie w bloku `mermaid` w sekcji poniżej (GitHub renderuje Mermaid w Markdown)
albo jako obraz w `docs/` z linkiem w tej sekcji. Usuńcie znaczniki TODO, gdy diagram będzie
gotowy — sprawdza to `python scripts/check_dod.py`.

<!-- DIAGRAM-V0:START -->
```mermaid
flowchart TD
    data["Dane ai4i2020.csv + kontrakt danych (S1)"]
    norm["normalize_input() (S1)"]
    filt["filter_training_rows() (S1)"]
    pipe["Pipeline: preprocessing + LogisticRegression (S1)"]
    model[("Model (plan)")]
    db[("Baza predykcji (plan)")]

    subgraph cloud["Cloud Run (plan)"]
        ui["UI (plan)"]
        api["API (plan)"]
    end

    data --> norm --> filt --> pipe --> model
    model -->|"wczytany raz przy starcie"| api
    ui -->|"Req: /predict"| api
    api -->|"Res: predykcja awarii 0/1 + prawdopodobieństwo"| ui
    api -->|"zapis predykcji"| db
```

Oznaczenia: (S1) — istnieje po Sprincie 1, (plan) — planowane w kolejnych sprintach.

- Dane `ai4i2020.csv` pobieramy z UCI Machine Learning Repository, a kontrakt danych (`datasets.yaml` + `project.yaml`) określa target i dozwolone cechy.
- `normalize_input()` ujednolica wejście (także w API), a `filter_training_rows()` tylko przy treningu usuwa rekordy bez targetu i duplikaty.
- Preprocessing i `LogisticRegression` tworzą jeden `Pipeline`, który zapiszemy jako model, a API wczyta go raz przy starcie.
- UI wysyła `POST /predict`, API zwraca predykcję awarii (0/1) z prawdopodobieństwem i zapisuje ją w bazie, a całość zostanie wdrożona w Cloud Run.
<!-- DIAGRAM-V0:END -->

## Historia zmian architektury

| Sprint | Zmiana | Powiązany ADR |
|---|---|---|
| S1 | diagram v0 | — |
