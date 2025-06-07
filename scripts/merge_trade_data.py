from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import country_converter as coco

# === Step 1: Load datasets ===
trade = pd.read_csv("/Users/hapham/critical-minerals-risk-index/data/raw/trade_data.csv")
stab = pd.read_csv("/Users/hapham/critical-minerals-risk-index/data/raw/stability_data.csv")
prod = pd.read_csv("/Users/hapham/critical-minerals-risk-index/data/raw/production_data.csv")

# === Step 2: Normalize column names ===
for df in [prod, trade, stab]:
    df.columns = df.columns.str.strip().str.lower()

coco_converter = coco.CountryConverter()
prod['country'] = coco_converter.convert(names=prod['country'], to='name_short')
trade['country'] = coco_converter.convert(names=trade['country'], to='name_short')
stab['country'] = coco_converter.convert(names=stab['country'], to='name_short')

prod['mineral'] = prod['mineral'].str.lower().str.strip()
trade['mineral'] = trade['mineral'].str.lower().str.strip()

# === Step 3: Prepare stability data ==
stab.rename(columns={'2023': 'stability_index'}, inplace=True)
stab = stab[['country', 'stability_index']].copy()
stab['stability_index'] = stab['stability_index'].astype(str).str.replace(',', '.').astype(float)

# == Step 4: Prepare trade data ==
producer_pairs = prod[['country', 'mineral']].drop_duplicates()
trade_filtered = trade.merge(producer_pairs, on=['country', 'mineral'], how='inner')

trade_volume = trade_filtered.groupby(['country', 'mineral'])['fobvalue'].sum().reset_index()

scaler = MinMaxScaler()
trade_volume['trade_concentration_index'] = scaler.fit_transform(trade_volume[['fobvalue']])

# == Step 5: Prepare production data ==
prod['mineral'] = prod['mineral'].str.lower().str.strip()

# == Step 8: Merge data
merged = prod.merge(trade_volume, on=['country', 'mineral'], how='left')
merged = merged.merge(stab[['country', 'stability_index']], on='country', how='left')
merged['stability_index'] = pd.to_numeric(merged['stability_index'], errors='coerce')
merged['political_risk_index'] = 100 - merged['stability_index']  # if stability was percentile

merged.dropna(subset=['stability_index', 'trade_concentration_index', 'political_risk_index'], inplace=True)

# == Step 9: Create political risk index
merged['political_risk_index'] = 1 - merged['stability_index']

# == Step 10: Drop rows with missing values
scaler = MinMaxScaler()
merged[['stability_scaled', 'trade_scaled', 'risk_scaled']] = scaler.fit_transform(
    merged[['stability_index', 'trade_concentration_index', 'political_risk_index']]
)

# == Step 11: Final risk score
merged['risk_score'] = (
    (1 - merged['stability_scaled']) * 0.4 +
    merged['trade_scaled'] * 0.3 +
    merged['risk_scaled'] * 0.3
)

# === Step 12: Save processed output ===
Path("data/processed").mkdir(parents=True, exist_ok=True)

merged.to_csv("data/processed/critical_minerals_risk.csv", index=False)

# Final confirmation
print("✅ Data processing complete. File saved to: data/processed/critical_minerals_risk.csv")












