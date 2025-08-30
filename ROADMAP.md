# 🗺️ AerialView Roadmap

This document outlines the planned improvements for **AerialView**, a finance analytics tool that provides stock market insights and visualizations in one click.

---

## 🎯 Project Goal
Deliver a **user-friendly, reliable, and insightful** stock analytics platform with:
- Interactive visualizations
- Clean, modular codebase
- Strong documentation and testing
- Easy setup and deployment

---

## ✅ Phase 1: Codebase & Structure
- [ ] Refactor into a package structure:

aerialview/
core/          # data fetching, transformations, visualization logic
app/           # Streamlit/Dash UI
utils/         # logging, helpers
tests/         # pytest-based tests

- [ ] Rename ambiguous files (`index.py` → `dashboard.py`).
- [ ] Add `__init__.py` and package imports.

---

## 📊 Phase 2: Visualization
- [ ] Implement **candlestick charts** with volume overlays.
- [ ] Add **moving averages (20/50-day)** and **Bollinger Bands**.
- [ ] Support **multi-ticker comparisons**.
- [ ] Create **correlation heatmaps** for multiple stocks.
- [ ] Improve aesthetics (titles, labels, tooltips).
- [ ] Add chart export (PNG/PDF).

---

## 📚 Phase 3: Documentation
- [ ] Expand `README.md`:
- Project overview
- Quickstart installation guide
- Example usage (`AAPL`, `TSLA`)
- Screenshots/GIF of dashboard
- Roadmap link
- [ ] Add Google-style **docstrings** to all functions.
- [ ] Create a `docs/` folder for future Sphinx/MkDocs.
- [ ] Add **contributing guide** and **issue/PR templates**.

---

## 🧪 Phase 4: Testing & Reliability
- [ ] Add **pytest** tests for:
- Data fetching
- Data transformations
- Visualization outputs
- [ ] Mock API calls to prevent flaky tests.
- [ ] Set up **GitHub Actions CI** for automated testing.
- [ ] Add coverage reporting (e.g., `pytest-cov`).

---

## 🛠️ Phase 5: Code Quality
- [ ] Integrate linters (`flake8`) and formatters (`black`, `isort`).
- [ ] Replace `print()` with `logging`.
- [ ] Add graceful error handling for:
- Invalid tickers
- Empty/missing data
- API/network failures

---

## 🌐 Phase 6: User Experience
- [ ] Streamlit dashboard with:
- Sidebar: ticker(s), date range, visualization options
- Main page: charts + KPIs
- [ ] CLI support:
```bash
python -m aerialview --ticker AAPL --start 2023-01-01 --end 2023-12-31
```
	•	Config file (config.json) for defaults.

⸻

🚀 Phase 7: Future Extensions
	•	Add technical indicators: RSI, MACD, volatility measures.
	•	Integrate news sentiment analysis.
	•	Portfolio simulation (risk/return, Sharpe ratio).
	•	Deploy demo to Streamlit Cloud or Heroku.
	•	Publish package on PyPI.

⸻

📌 Milestones
	•	M1: Clean structure, working dashboard with candlestick & moving averages.
	•	M2: Documentation + testing suite.
	•	M3: CI/CD pipeline + deployment.
	•	M4: Advanced indicators + portfolio features.

⸻

📝 Notes

This roadmap is iterative — features may be adjusted based on user needs and contributions.