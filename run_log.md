# Run log

Everything the paper must report. Fill in as you go; never edit past entries, add new ones.

## Environment

| Item | Value |
|---|---|
| Python | |
| torch / CUDA | |
| transformers | |
| GPU | (e.g. Colab T4 16 GB, fp16) |
| requirements.lock.txt saved | no |

## Data sources

| Item | Value |
|---|---|
| Wikidata query date (coverage_gap.sparql) | |
| Wikidata query date (build_dataset.py) | |
| Tamil Wikipedia access date | |
| Endpoint | https://query.wikidata.org/sparql |

## Models

| Role | Model ID | HF revision / API version | Precision | Date recorded |
|---|---|---|---|---|
| SLM, base, few-shot | Sarvam-1 (2B) | | fp16 | |
| SLM, instruct 3-4B | | | fp16 | |
| Large LLM (API, upper bound) | | access date: | n/a | |
| Translation (RQ1b) | | | | |
| Standby: Agaram 2.5B Instruct | not used | | | |

## Decisions taken during the work

| Date | Decision | Why |
|---|---|---|

## Runs

| Date | Script + args | Input | Output | Notes / numbers |
|---|---|---|---|---|
