# StatForge

StatForge is a personal macro data warehouse and analysis toolkit.

It pulls raw, non-sensationalized data from official sources (StatsCan, Bank of Canada, CMHC, etc.), loads it into a clean dimensional model in Postgres, and exposes it through a Panel web app for interactive exploration and personal decision making.

---

## Features (MVP)

- Ingest time series data from:
  - Statistics Canada Web Data Service
  - Bank of Canada Valet API
  - CMHC housing data (CSV or API where available)
- Store data in a dimensional model:
  - `dim_series`, `dim_geo`, `dim_date`, `fact_observation`
- Basic ETL pipeline in Python:
  - `extract/` modules per source
  - `transform/` for cleaning and normalization
  - `load/` for writing into Postgres
- Panel web UI:
  - Series explorer with filters for metric, geography, and date range
  - First “app”: housing affordability / rent vs buy playground

Planned:

- More series and topics (labour, income, inflation, debt)
- Scenario tools for personal finance and long term planning
- Optional API layer for future integrations

---

## Project structure

High level layout:

```text
statforge/
├── docker/
│   ├── panel.Dockerfile
│   ├── worker.Dockerfile
│   └── api.Dockerfile         # optional, future
│
├── docker-compose.yml
│
├── src/
│   └── statforge/
│       ├── __init__.py
│       ├── config/
│       │   ├── settings.py
│       │   └── secrets_template.env
│       │
│       ├── etl/
│       │   ├── extract/
│       │   ├── transform/
│       │   └── load/
│       │
│       ├── db/
│       │   ├── models.py
│       │   └── init_db.py
│       │
│       ├── panel/
│       │   ├── app.py
│       │   └── pages/
│       │       ├── home.py
│       │       ├── explorer.py
│       │       └── affordability.py
│       │
│       ├── api/               # optional
│       ├── utils/
│       └── tests/
│
├── alembic/                    # if using migrations
├── requirements.txt or pyproject.toml
├── .env                        # local only, not committed
├── .gitignore
└── README.md
