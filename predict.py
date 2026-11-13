"""
predict.py — Run the trained Supply Chain ML models
=====================================================
Usage:
  python predict.py                  # runs on a sample from the dataset
  python predict.py --csv my_data.csv   # runs on your own CSV file
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import argparse
import pickle
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────
CLS_MODEL_PATH = r"models\best_classifier.pkl"
REG_MODEL_PATH = r"models\best_regressor.pkl"
DEFAULT_DATA   = r"dynamic_supply_chain_logistics_dataset.csv"

# ── Load models ────────────────────────────────────────────────────────
print("\nLoading models...")
with open(CLS_MODEL_PATH, "rb") as f:
    cls_bundle = pickle.load(f)

with open(REG_MODEL_PATH, "rb") as f:
    reg_bundle = pickle.load(f)

cls_model    = cls_bundle["model"]
label_enc    = cls_bundle["label_encoder"]
feature_cols = cls_bundle["feature_cols"]   # 23 feature names

reg_model    = reg_bundle["model"]

print(f"  Classifier : {cls_bundle['model_name']}")
print(f"  Regressor  : {reg_bundle['model_name']}")
print(f"  Features   : {len(feature_cols)}")

# ── Load data ──────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--csv", default=None, help="Path to a CSV file for prediction")
parser.add_argument("--rows", type=int, default=10, help="Number of sample rows to predict (default: 10)")
args = parser.parse_args()

if args.csv:
    print(f"\nLoading data from: {args.csv}")
    df = pd.read_csv(args.csv)
else:
    print(f"\nNo --csv provided. Using {args.rows} sample rows from the default dataset.")
    df = pd.read_csv(DEFAULT_DATA).sample(args.rows, random_state=42)

# ── Prepare features ───────────────────────────────────────────────────
missing = [c for c in feature_cols if c not in df.columns]
if missing:
    print(f"\n[ERROR] Your CSV is missing these required columns:\n  {missing}")
    sys.exit(1)

X = df[feature_cols].values

# ── Predict ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("PREDICTIONS")
print("=" * 60)

# Classification
cls_preds     = cls_model.predict(X)
cls_labels    = label_enc.inverse_transform(cls_preds)
cls_proba     = cls_model.predict_proba(X)          # probabilities

# Regression — Ridge uses scaled data
scaler = cls_bundle["scaler"]
X_sc   = scaler.transform(X)
reg_preds = reg_model.predict(X_sc)

# ── Display results ────────────────────────────────────────────────────
results = df[feature_cols].copy().reset_index(drop=True)
results["predicted_risk"]               = cls_labels
results["risk_confidence_%"]            = (cls_proba.max(axis=1) * 100).round(1)
results["predicted_delivery_deviation"] = reg_preds.round(3)

# Show a compact summary
summary = results[["predicted_risk", "risk_confidence_%", "predicted_delivery_deviation"]]
print(summary.to_string(index=True))

print("\n" + "=" * 60)
print("Risk class distribution:")
print(results["predicted_risk"].value_counts().to_string())

# ── Save results ───────────────────────────────────────────────────────
out_path = "predictions_output.csv"
results.to_csv(out_path, index=False)
print(f"\nFull results saved -> {out_path}")
print("Done!")
