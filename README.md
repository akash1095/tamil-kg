# Neuro-Symbolic KG Construction and QA for Tamil with Small Language Models

Code and data for an anonymous SPELLL 2027 submission.
Keep this repository anonymous: no names, affiliations, e-mails or personal paths
in code, comments, data or commit messages.

## Layout

```
scripts/            one script per step; JSONL in, JSONL out
data/raw/           Wikidata facts and Tamil Wikipedia intros (build_dataset.py)
data/annotation/    annotate.csv, guidelines.md, second-annotator file
data/splits/        dev.jsonl (50), test.jsonl (150), *_en.jsonl translations
data/cache/         cached SPARQL/API responses (git-ignored)
results/coverage/   coverage_gap.sparql output
results/rq1/        extraction predictions + scores (3 models x 2 settings)
results/rq2/        validated triples, rejection log, scores
results/rq3/        QA answers + scores (3 models x 3 conditions)
run_log.md          model versions, query dates, every run
```

## Pipeline

| Step | Script | In | Out |
|---|---|---|---|
| Coverage statistic | `coverage_gap.sparql` | Wikidata | `results/coverage/` |
| Dataset | `build_dataset.py` | Wikidata, Tamil Wikipedia | `data/raw/candidates.jsonl`, `data/annotation/annotate.csv` |
| Split | `split_dataset.py` | `annotate.csv` | `data/splits/dev.jsonl`, `test.jsonl` |
| Agreement | `kappa.py` | annotation files | kappa |
| Translate | `translate.py` | `*.jsonl` | `*_en.jsonl` |
| Extract (RQ1) | `extract.py --model M --setting direct\|translate` | splits | `results/rq1/` |
| Entity linking | `link_entities.py` | predictions | linked predictions |
| Score RQ1 | `evaluate_extraction.py` | predictions, gold | scores |
| Validate (RQ2) | `validate.py` | linked predictions | validated + rejections |
| Score RQ2 | `evaluate_validation.py` | before/after | scores |
| Questions (RQ3) | `make_questions.py` | `test.jsonl` | `questions.jsonl` |
| QA (RQ3) | `qa.py --model M --condition closed\|ours\|gold` | questions, KG | `results/rq3/` |
| Score RQ3 | `evaluate_qa.py` | answers | scores |

## Setup

```
pip install -r requirements.txt
cp .env.example .env   # add the API key
```
