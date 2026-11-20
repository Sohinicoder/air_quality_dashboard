# Air-Quality Observation Dashboard (Project 5)

## Overview
This project is an end-to-end Python data pipeline that analyzes daily fine-particle air pollution (PM2.5) readings across two campus monitoring stations (`ST-01` and `ST-02`). It generates a reproducible simulated dataset, validates readings using Object-Oriented Programming, detects anomalies statistically with NumPy, summarizes data with Pandas, and visualizes trends using Matplotlib.

## Project Files
* `main.py` — Main Python script containing the data simulation, validation class, analysis pipeline, and plotting logic.
* `README.md` — Project documentation and setup instructions.
* `Project_Report.pdf` — Detailed capstone project report.
* `simulated_air_quality.csv` — Generated dataset containing 30 days of simulated PM2.5 readings (including intentional anomalies and invalid values).
* `monthly_summary.json` — Exported Pandas summary of mean, max, and valid reading counts per station.
* `air_quality_analysis.png` — Dual-panel visualization showing daily PM2.5 trends and reading distributions.

## How to Run (Windows)
1. **Open the project folder** (`air_quality_dashboard`) in VS Code.
2. **Create and activate a virtual environment** in the terminal:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate