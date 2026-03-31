# The decline of The Simpsons

This repository contains the first practical work for the Data Visualization course. The project explores how *The Simpsons* has evolved over time, focusing on the relationship between episode ratings, audience size, season-by-season distributions, and broadcast patterns.

## Repository contents

- `simpsons_episodes.csv`: original dataset.
- `simpsons_episodes_clean.csv`: cleaned dataset used by the visualizations.
- `simpsons_cleaning_notebook_adriansegura_pablorodriguez.ipynb`: notebook used to clean and enrich the original data.
- `charts_adriansegura_pablorodriguez.ipynb`: exploratory charts and design decisions developed during the analysis.
- `dashboard_adriansegura_pablorodriguez.py`: Streamlit dashboard for the final interactive visualization.


## How to run

Install the required libraries in your environment:

```bash
pip install streamlit pandas altair numpy
```

Launch the dashboard with:

```bash
streamlit run dashboard_adriansegura_pablorodriguez.py
```

or

```bash
python -m streamlit run dashboard_adriansegura_pablorodriguez.py
```

## Data preparation

If you need to regenerate the cleaned dataset, open `simpsons_cleaning_notebook_adriansegura_pablorodriguez.ipynb` and run all cells. This produces `simpsons_episodes_clean.csv`, which is the file consumed by the dashboard.

## Notes

- The dashboard expects `simpsons_episodes_clean.csv` to be in the project root.
- File names are case-sensitive in some environments. The exploratory notebook is `charts_adriansegura_pablorodriguez.ipynb`.
