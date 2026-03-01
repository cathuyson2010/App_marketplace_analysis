# Google Play Store App Analysis

A comprehensive data analysis project examining the Google Play Store dataset to identify market opportunities, category performance, and app success metrics.

## Project Overview

This analysis explores:
- Overall market structure and dataset composition
- App category ratings and user satisfaction patterns
- Install distribution and market size by category
- Detailed examination of top-performing categories
- Strategic insights for app development decisions

## Dataset

- **Source**: Google Play Store
- **Records**: 10,841 apps
- **Features**: 13 columns including App name, Category, Rating, Reviews, Size, Installs, and more

## Project Structure

```
notebooks/
├── Reading_data_in_general.ipynb  # Data loading and general exploration
└── GAME.ipynb                      # GAME category deep-dive analysis
```

## Analysis Highlights

### Data Overview
The dataset contains comprehensive app information across multiple dimensions:
- App ratings (0-5.0 scale)
- User review counts
- Installation numbers
- App categories and genres
- Pricing models (Free/Paid)
- Content ratings and Android version requirements

### GAME Category Analysis
The GAME category analysis includes:
- Top performing games with install metrics
- Rating distributions and user engagement
- App sizes and memory requirements
- Popular game genres (Arcade, Casual, Action, Strategy, etc.)
- Notable games: Subway Surfers (1B+ installs), Candy Crush Saga (500M+ installs), Clash Royale

### Market Insights
- **Game Market Leadership**: GAME category represents the largest market segment with 35 billion installs
- **High-Volume Categories**: Communication (32.6B installs) and Productivity (14.2B installs) also show strong performance
- **Quality Leaders**: Education, Books & Reference, and Personalization categories demonstrate highest average ratings

## How to Run

### Prerequisites
```bash
pip install pandas numpy jupyter
```

### Execute Analysis
```bash
jupyter notebook notebooks/Reading_data_in_general.ipynb
jupyter notebook notebooks/GAME.ipynb
```

## Data Processing

The analysis includes:
- Data validation and quality checks
- Handling missing values (13.5% missing ratings)
- Removal of anomalous ratings (>5.0)
- String-to-numeric conversion for install counts
- Category and genre standardization

## Key Findings

1. **Market Dominance**: The GAME category dominates in total installs but faces intense competition
2. **Quality vs. Volume**: Education and Books categories offer quality alternatives with lower saturation
3. **Install Variability**: Top games show massive installation bases while many apps have minimal adoption
4. **Rating Consistency**: Most apps with sufficient reviews cluster around 4.0-4.5 ratings

## Author

**cathuyson2010**

## License

This project is open source and available under the MIT License.