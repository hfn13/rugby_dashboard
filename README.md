# Rugby Matchday Statistics Dashboard (Detailed)

## Overview
This project is a **Streamlit-based analytics dashboard** designed to analyse rugby match data collected in Excel spreadsheets.  
It compares **Middlesbrough RFC** performance against multiple opponents across a season and provides:
- Team KPIs
- Match comparisons
- Attack & defence breakdowns
- Event-based match reports

The app is intended for **performance analysis**, **coaching insights**, and **post-match review**.

---

## Data Sources
- Excel files containing one sheet per team per match
- Each sheet represents event-based match data (passes, tackles, carries, kicks, set pieces, etc.)

### File Structure
- One workbook per match
- Sheet names match team names
- Example:
  - `Middlesbrough`
  - `Ilkley`
  - `York`

---

## Libraries Used
- `streamlit` – interactive dashboard UI
- `pandas` – data manipulation
- `matplotlib / seaborn` – static visualisations
- `plotly.express` – interactive plots

---

## Data Loading & Preparation
- Home and opponent datasets are loaded separately
- Missing values are filled with zeros
- Multiple matches are concatenated to allow:
  - Season-wide analysis
  - Comparison between latest match and previous matches

---

## Carry & Kick Encoding System
Distances are stored as **letter codes** rather than raw numbers.

Example:
- `A` → 0–5m
- `B` → 5–20m
- `C` → 20–30m
- `Z` → Negative carry
- `X` → Dropped ball

Each letter is mapped to an **average distance value**, enabling numeric analysis.

---

## Core Helper Functions

### `distance_avg()`
Converts encoded carry or kick strings into an **average distance in metres**.

### `count_line_breaks()`
Counts carries exceeding 5 metres to estimate line breaks.

### `get_values()`
Extracts numeric distance values from encoded kick/carry sequences.

### `get_time()`
Converts raw seconds into `MM:SS` format.

---

## Dashboard Structure

### Sidebar Navigation
- Home (Season overview)
- Individual opponent pages

---

## Home View
### Boro Statistics
Displays:
- Tries & conversion rates
- Pass accuracy
- Tackle completion
- Set piece success
- Carry metres & errors
- Line breaks
- Kick counts

Each KPI includes:
- Total value
- Delta vs previous match

### Boro Analyses
Displays:
- Machine learning: Use of permutation importance to rank which features are driving performance.
- Correlation: Find out which features were truly driving performance, that is, leading to scoring and conceding of tries.
  
### Opponent Statistics and Analyses
Same KPIs, but aggregated for all opponents.

---

## Match-Level Analysis
For each opponent:
- Overview tab
- Match Report tab

### Overview
- Team vs team KPI comparison
- Attack & Defence segmentation
- Visual bar comparisons

### Match Report
- Event-based timeline
- Tries, penalties, halftime, fulltime
- Snapshot KPIs at each event moment
- Use of Markov Chains to explain team performance based on carry metre sequence
---

## Visualisations
- KPI metric cards
- Comparison bar charts
- Custom HTML/CSS stat cards for head-to-head display

---

## Intended Use
- Coaching review
- Performance benchmarking
- Tactical decision-making
- Season trend analysis

---

## Future Improvements
- Player-level analytics
- Expected metres / expected tries
- Machine learning predictions
- Database-backed storage
