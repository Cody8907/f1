# 🏎️ Formula 1 Analytics Dashboard

A Streamlit dashboard for exploring Formula 1 history — driver performances, podium finishes, and team statistics.

## Features

- 📅 **Season filter** — pick any year from the sidebar
- 🏆 Top metrics: championship leader and top team for the selected season
- 📊 **Driver Standings** — top 10 drivers by points (interactive Plotly bar chart)
- 🥧 **Team Comparison** — constructor points distribution (pie chart)

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data

The `data/` folder contains CSV extracts (races, results, drivers, constructors) sourced from the [Ergast F1 dataset](https://www.kaggle.com/datasets/cmcgrady/ergast-f1-race-data-19502023).

## Tech stack

- Python, Streamlit, pandas, Plotly Express
