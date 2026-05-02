# Consultations Scraper — Tasks

## How to use this file

Read CONTEXT.md first, then work through tasks top-to-bottom.

---

### 1. [ ] Revive: confirm cron status, test scripts, refresh feeds
**Description**: The project has been dormant since March 2025. Steps:
1. Check `crontab -l` for any existing entries — there probably are none
2. Run `python scripts/corkcounty.py` and `python scripts/tipp.py` from the project root (or with a venv if dependencies are installed) — check for errors; council site structures may have changed
3. If scripts run successfully, refresh both feeds and verify the RSS XML looks correct
4. Add a cron entry to run both scrapers on a regular schedule (e.g. daily)
5. Update CONTEXT.md to reflect active cron schedule

---

### 2. [ ] Add pyproject.toml and standard venv
**Description**: Dependencies (`requests`, `beautifulsoup4`, `python-dateutil`, `pytz`) are currently implicit — no `pyproject.toml` or `requirements.txt`. Add a `pyproject.toml` following the project standard so dependencies are explicit and reproducible. Use `uv` for venv management.

---

### 3. [ ] Apply routekit branding to index.html
**Description**: `index.html` has no routekit branding. Apply:
1. Add `<link rel="stylesheet" href="https://projects.bibby.ie/routekit/routekit.css">`
2. Add `<script src="https://projects.bibby.ie/routekit/navbar.js"></script>`
3. Wrap content in standard routekit page structure (`.page-header`, `.container`, `.card`)

---

### 4. [ ] Expand to additional councils
**Description**: Consider adding more councils where planning notices are relevant to public transport infrastructure. Candidates: Dublin City Council, Dún Laoghaire–Rathdown, Fingal, South Dublin, Galway City, Limerick. Evaluate whether council sites are scrapeable (structured HTML vs. PDF-only) before committing.

---

### 5. [ ] Graduate to navbar (Data menu — Tools section)
**Description**: Once branding is applied and feeds are active, add to the RouteKit ecosystem:
1. Add `Consultations Scraper` to navbar Data → Tools section
2. Add tool card to routekit landing page (Data section)
3. Move from *Not yet integrated* to *Integrated* in `routekit/CONTEXT.md`
