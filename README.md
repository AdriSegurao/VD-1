# The decline of The Simpsons

This repository contains the first practical work for the Data Visualization course. The project explores how *The Simpsons* has evolved over time, focusing on the relationship between episode ratings, audience size, season-by-season distributions, and broadcast patterns.

## Repository contents

- `simpsons_episodes.csv`: original dataset.
- `simpsons_episodes_clean.csv`: cleaned dataset used by the visualizations.
- `simpsons_cleaning_notebook.ipynb`: notebook used to clean and enrich the original data.
- `charts.ipynb`: exploratory charts and design decisions developed during the analysis.
- `dashboard.py`: Streamlit dashboard for the final interactive visualization.

## Dashboard overview

The dashboard is titled **The decline of The Simpsons** and includes:

- viewers distribution by season
- ratings distribution by season
- heatmap of viewers by season and episode number
- heatmap of ratings by season and episode number
- weekday viewers boxplot
- weekday episode count bar chart
- correlation chart between IMDb rating and US viewers

## How to run

Install the required libraries in your environment:

```bash
pip install streamlit pandas altair numpy
```

Launch the dashboard with:

```bash
streamlit run dashboard.py
```

## Data preparation

If you need to regenerate the cleaned dataset, open `simpsons_cleaning_notebook.ipynb` and run all cells. This produces `simpsons_episodes_clean.csv`, which is the file consumed by the dashboard.

## Notes

- The dashboard expects `simpsons_episodes_clean.csv` to be in the project root.
- File names are case-sensitive in some environments. The exploratory notebook is `charts.ipynb`.
