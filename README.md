# 📈 AerialView

AerialView is a finance analytics tool that provides **stock market insights and visualizations in one click**.  
It fetches historical data, computes technical indicators, and generates **interactive charts** for one or multiple stocks.

---

## 🚀 Features
- Fetch historical stock data (Yahoo Finance / Alpha Vantage).
- Visualizations:
  - Candlestick charts with volume overlays.
  - Moving averages (20/50-day) and Bollinger Bands.
  - Multi-ticker comparison plots.
  - Correlation heatmaps.
- Export charts as PNG/PDF.
- Streamlit dashboard for interactive exploration.
- CLI option for quick analysis.

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/BugVanquisher/AerialView.git
cd AerialView
pip install -r requirements.txt
```

---

## ▶️ Usage

Run Dashboard
```
streamlit run aerialview/app/dashboard.py
```
CLI Mode
```
python -m aerialview --ticker AAPL --start 2023-01-01 --end 2023-12-31
```

---

## 📊 Example Visuals

Candlestick Chart

Correlation Heatmap


---

## 📚 Documentation

Each function includes Google-style docstrings.
For more details, check the docs/ folder (coming soon).

---

## 🧪 Testing

Run tests with:
```
pytest
```
Tests cover:
	•	Data fetching
	•	Transformations
	•	Visualization outputs

---

## 📌 Roadmap

See ROADMAP.md for planned improvements:
	•	Project refactor
	•	New indicators (RSI, MACD)
	•	Portfolio analysis
	•	Live deployment on Streamlit Cloud

---

## 🤝 Contributing

Contributions welcome!
Please see CONTRIBUTING.md (to be added) for guidelines.

---

## 📜 License

MIT License © 2025 BugVanquisher

---

## Screenshots

### UI v2
![Stock for Apple](https://github.com/JuneSunshine/AerialView/blob/master/assets/screenshot_v2.png)


### UI v1
![Stock for Apple](https://github.com/JuneSunshine/AerialView/blob/master/assets/screenshot_v1.png)