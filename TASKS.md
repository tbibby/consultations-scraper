# Consultations Scraper — Notes

This project is dormant (see CONTEXT.md). The items below were open tasks,
kept here as notes in case the project is revived.

---

### Revive: confirm cron status, test scripts, refresh feeds
The project was dormant since March 2025. Reviving would mean: checking for
existing cron entries (likely none), running `scripts/corkcounty.py` and
`scripts/tipp.py` to check whether council site structures still match what
the scrapers expect, refreshing both RSS feeds, and adding a cron schedule.

### Add pyproject.toml and standard venv
Dependencies (`requests`, `beautifulsoup4`, `python-dateutil`, `pytz`) are
implicit — no `pyproject.toml` or `requirements.txt`. Should use `uv` for venv
management if this project follows the current project standard.

### Apply routekit branding to index.html
`index.html` has no routekit branding. Would need the routekit stylesheet/navbar
script and standard page structure (`.page-header`, `.container`, `.card`).

### Expand to additional councils
Candidates considered for public-transport-relevant planning notices: Dublin
City Council, Dún Laoghaire–Rathdown, Fingal, South Dublin, Galway City,
Limerick. Would need to evaluate whether each site is scrapeable (structured
HTML vs. PDF-only).

### Graduate to navbar (Data menu — Tools section)
Once branding is applied and feeds are active: add to navbar Data → Tools
section, add a tool card to the routekit landing page, and move from *Not yet
integrated* to *Integrated* in `routekit/CONTEXT.md`.
