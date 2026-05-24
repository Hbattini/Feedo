# Ingestion Pipeline

## Decision

Open Pet Food Facts is the MVP food source. Raw payloads are untrusted and stored separately before normalization.

## Pipeline

```txt
fetch
normalize
validate
enrich
dedupe
persist
generate feature_json
increment catalog_version
```

## Rules

- Enrichment is deterministic parser logic only.
- LLMs are not used for ingestion.
- Records missing or unable to map life stage are rejected from the active catalog.
- Feature JSON is generated from canonical normalized attributes and never manually edited.
- The recommendations app never mutates food data.

## MVP Execution

Ingestion runs through Django management commands. Celery is deferred.
