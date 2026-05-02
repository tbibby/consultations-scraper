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

Dormant since March 2025 (~14 months). No active cron job. Feeds were last generated manually. The scraping approach was working at the time; council site structures may have changed.

## Note on version control

This directory contains a nested `.git` repo (predates the monorepo). The `rss/` output directory is gitignored in the inner repo.

## Dependencies

`requests`, `beautifulsoup4`, `python-dateutil`, `pytz` — no `pyproject.toml` yet, dependencies are implicit.

## Getting Your Task

Read `TASKS.md` and find the first task marked `[ ]`. Implement it, then confirm with the user before marking `[x]`. After marking done, commit and push. Do not include any references to Claude Code or AI in commit messages.
