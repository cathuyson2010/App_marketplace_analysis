# SQL analysis (MySQL 8.0+)

## Run

1. Open and execute 01_create_database.sql in MySQL Workbench.
2. Configure mysql_config_editor login path app_marketplace on your machine.
3. From the repository root run: python sql/import_cleaned.py
4. Run 02_data_validation.sql, then 03_business_analysis.sql in Workbench.

The importer uses the MySQL command-line client and Python standard library.
Use --mysql to specify a different mysql executable and --login-path for another saved login.
No password is stored in the repository.
Import uses UTF-8 hex literals, explicit column mapping and 250-row batches.
All 13 fields of every row are compared with CSV before an atomic table rename.
Every successful import retains the old table as apps_backup_TIMESTAMP.
An import failure leaves the active apps table untouched.
Original SQL drafts in data/ are preserved; sql/ is the maintained workflow.

## Verified repair: 2026-09-07

Before repair, apps had 317 rows and only 7 categories.
The cleaned CSV contains 8,196 rows and 33 categories.
This demonstrates incomplete import, not a GAME-only problem.
The exact original Wizard error was not available; no claim is made about its trigger.
The original table remains as apps_backup_20260907_135303.
After repair all 8,196 rows and all 13 source fields matched the CSV.
There are no duplicate app names, invalid ratings, negative numeric values,
missing categories, missing ratings, or missing install counts in this export.

## Verified findings

| Category | Apps | Installs |
|---|---:|---:|
| GAME | 912 | 13,878,762,717 |
| COMMUNICATION | 256 | 11,038,241,530 |
| TOOLS | 718 | 7,999,724,500 |
| PRODUCTIVITY | 301 | 5,793,070,180 |
| SOCIAL | 203 | 5,487,841,475 |

GAME has 836 Free apps (mean rating 4.236) and 76 Paid apps (4.372).
Free GAME installs total 13,857,763,455 versus Paid 20,999,262.
Higher paid ratings are descriptive; they do not establish a pricing effect.
All 12 business queries executed successfully on MySQL 8.0.46.

## Interpretation and limitations

This cleaned export excludes missing ratings; results describe the rated-app sample.
Installs are cumulative lower-bound buckets, not exact downloads or time-series growth.
App counts measure supply in this sample, not complete market competition.
Top-three share and mean/median comparisons describe concentration.
Shortlist niches for further research; the dataset cannot prove startup safety,
profitability, passive income, retention, acquisition cost or subscription potential.
Do not label price multiplied by installs as observed revenue.
The JOIN query uses category benchmarks derived from the same table.
Sample thresholds (50 rated apps / 5 paid apps) are analytical choices.
