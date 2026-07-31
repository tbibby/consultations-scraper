# Consultations Scraper — Context

## What is this?

A set of Python scripts that scrape Irish local authority consultation pages and generate RSS feeds. The feeds let planners subscribe to planning notices (Part 8, Section 38, general consultations) without manually checking council websites.

## Current feeds

| Feed | Source | Output |
|------|--------|--------|
| Cork County Council (Section 38 + Part 8) | `corkcoco.ie` | `rss/corkcounty.rss.xml` |
| Tipperary County Council | `consultations.tipperarycoco.ie` | `rss/tipperary.rss.xml` |

The `index.html` at the project root lists links to both feeds.

## Architecture

No Flask — pure Python scripts that write static XML files. Intended to be run on a cron schedule.

- Scripts live in `scripts/`
- RSS output goes to `rss/` (gitignored)
- `index.html` is the static landing page

### Key files

| File | Purpose |
|------|---------|
| `scripts/corkcounty.py` | Scrapes Cork County Council Section 38 and Part 8 pages, visits each consultation URL to extract dates, generates RSS |
| `scripts/tipp.py` | Scrapes Tipperary County Council open consultations; also exports `description_escaped_html()` used by corkcounty.py |
| `scripts/extract_dates.py` | Date extraction helper: finds earliest and latest dates in free text (used by Cork County scraper) |
| `scripts/detect_date_in_fragments.py` | Date detection experiments |
| `index.html` | Static HTML landing page listing the RSS feeds |
| `rss/corkcounty.rss.xml` | Generated Cork County feed |
| `rss/tipperary.rss.xml` | Generated Tipperary feed |

## Apache

No explicit Apache config — served via DocumentRoot fallback at `/consultations-scraper/`. The `rss/` subdirectory is accessible at `/consultations-scraper/rss/`.

## Status

Dormant since March 2025. No active cron job. Feeds were last generated manually. The scraping approach was working at the time; council site structures may have changed.

**2026-07-31**: `../part8` now exists as a more authoritative Part 8 scraper, pulling all 31 councils directly from the LGMA planning portal (`planning.localgov.ie`). This project's Part 8 coverage (Cork, Tipperary) is superseded by `../part8`. However, `../part8` does not cover **Section 38** consultations — this project's Cork County scraper is currently the only thing covering Section 38. Keeping this project around as dormant rather than retiring it, in case we want to reopen it to specifically cover Section 38 (dropping the now-redundant Part 8 scraping). Open tasks moved to notes in TASKS.md.

## Note on version control

This directory contains a nested `.git` repo (predates the monorepo). The `rss/` output directory is gitignored in the inner repo.

## Dependencies

`requests`, `beautifulsoup4`, `python-dateutil`, `pytz` — no `pyproject.toml` yet, dependencies are implicit.

## Getting Your Task

This project is dormant — there are no active tasks. `TASKS.md` holds notes on
previously open work, kept for reference if the project is reopened (see
Status above). Don't act on them without checking with the user first.
