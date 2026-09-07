# Executive summary
## Decision

Use this analysis to shortlist categories for customer research, not to select a
guaranteed safe or profitable business model.

## Evidence

The cleaned rated-app sample contains 8,196 apps across 33 categories.
GAME leads total reported installs at 13.879B, but its median is 1M versus a 15.22M mean.
COMMUNICATION has a 1M median and 43.12M mean, illustrating even greater skew.
EDUCATION averages 4.364 in ratings versus GAME's 4.247.
However, EDUCATION's top-three install share is 34.01%, above GAME's 14.41%.
High ratings therefore do not establish lower concentration or safer entry.
Paid games average 4.372 in ratings versus 4.236 for Free games, with much lower
aggregate installs. Price effects cannot be separated from other factors here.

## Recommended next research

Interview potential users in a narrowly defined niche, then collect retention,
acquisition cost, willingness to pay, maintenance effort and actual revenue.
Evaluate business feasibility with those measures before selecting a monetization model.

## Reproducibility and scope

Run both notebooks, scripts/build_portfolio_report.py and the SQL workflow.
All 13 CSV fields were reconciled against MySQL for 8,196 records.
Installs are cumulative lower-bound buckets. Unrated apps are excluded.
App-name deduplication is imperfect without package identifiers.
The original CSV provenance/license needs to be recorded before further data redistribution.
