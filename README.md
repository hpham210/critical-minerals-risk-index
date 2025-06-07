# critical-minerals-risk-index
Risk index analysis of critical mineral supply chains
# 🌍 Critical Minerals Risk Index Dashboard

This project builds a data pipeline and interactive dashboard to assess geopolitical and supply chain risk across countries for strategic minerals (like lithium, cobalt, and rare earths).

🔗 **Live Dashboard**: [View on Tableau Public](https://public.tableau.com/app/profile/ha.pham3837/viz/shared/R5PQD5JRK)

---

## 💡 Objective

To quantify and visualize risk exposure across countries and minerals by combining:
- Political stability (World Bank percentile rank)
- Trade concentration (FOB export values)
- Supply-side production data

---

## 🛠️ Tools Used

- **Python**: `pandas`, `scikit-learn`, `country_converter`
- **Tableau**: interactive dashboards and filters
- **GitHub**: version control and portfolio hosting

---

## 🧪 Risk Score Calculation

```python
risk_score = (
    (1 - stability_scaled) * 0.4 +
    trade_scaled * 0.3 +
    risk_scaled * 0.3
)
