# Google Play Store App Analysis

A data analysis project examining the Google Play Store dataset to identify market opportunities and top-performing app categories.

##  Project Overview

This analysis explores:
- App category ratings and user satisfaction
- Market size distribution across categories
- Strategic insights for app development decisions

##  Dataset

- **Source**: Google Play Store
- **Records**: 10,841 apps
- **Columns**: 13 (App name, Category, Rating, Reviews, Size, etc.)

##  Key Findings

### Top-Rated Categories (100+ apps)
1. **EDUCATION** - 4.39/5.0 rating
2. **BOOKS_AND_REFERENCE** - 4.35/5.0 rating
3. **PERSONALIZATION** - 4.34/5.0 rating

### Largest Markets
1. **GAME** - 35 billion installs
2. **COMMUNICATION** - 32.6 billion installs
3. **PRODUCTIVITY** - 14.2 billion installs

##  How to Run

### Prerequisites
```bash
pip install pandas numpy jupyter
```

### Execute
```bash
jupyter notebook notebooks/googleplaystore.ipynb
```

##  Data Cleaning

The analysis handles:
-  Removed anomalous ratings (>5.0)
-  Removed rows with missing ratings (13.5%)
-  Converted string installs to numeric values
-  Data validation and quality checks

##  Business Insights

- **High Quality + High Demand**: EDUCATION category offers best opportunity
- **Market Saturation**: GAME category dominates but has intense competition
- **Strategic Opportunity**: BOOKS_AND_REFERENCE has good ratings with moderate competition

##  Author

**cathuyson2010**

##  License

This project is open source and available under the MIT License.