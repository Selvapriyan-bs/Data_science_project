"""
Supply Chain Logistics ML Pipeline
====================================
Trains and compares multiple models for:
  1. Classification  -> risk_classification (Low / Moderate / High Risk)
  2. Regression      -> delivery_time_deviation (hours)

Outputs:
  - models/best_classifier.pkl
  - models/best_regressor.pkl
  - reports/model_report.txt
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
import warnings
import pickle
import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score
)

# Classifiers
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import lightgbm as lgb

# Regressors
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
DATA_PATH   = r"dynamic_supply_chain_logistics_dataset.csv"
MODEL_DIR   = "models"
REPORT_DIR  = "reports"
PLOT_DIR    = "plots"
RANDOM_STATE = 42
TEST_SIZE    = 0.20
CV_FOLDS     = 5

os.makedirs(MODEL_DIR,  exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR,   exist_ok=True)

report_lines = []

def log(msg=""):
    print(msg)
    report_lines.append(msg)

# ─────────────────────────────────────────────
# 1. LOAD & PREPROCESS
# ─────────────────────────────────────────────
log("=" * 65)
log("SUPPLY CHAIN LOGISTICS — ML PIPELINE")
log("=" * 65)
log()
log(">> Loading dataset …")

df = pd.read_csv(DATA_PATH)
log(f"  Rows: {len(df):,}  |  Columns: {df.shape[1]}")

# Drop timestamp (not a predictive feature in tabular ML)
df = df.drop(columns=["timestamp"], errors="ignore")

# Encode target for classification
le = LabelEncoder()
df["risk_classification_enc"] = le.fit_transform(df["risk_classification"])
class_names = le.classes_

log(f"  risk_classification classes: {class_names.tolist()}")
log(f"  delivery_time_deviation range: [{df['delivery_time_deviation'].min():.2f}, {df['delivery_time_deviation'].max():.2f}]")
log()

# Feature matrix (exclude both target columns)
DROP_COLS   = ["risk_classification", "risk_classification_enc", "delivery_time_deviation"]
FEATURE_COLS = [c for c in df.columns if c not in DROP_COLS]

X = df[FEATURE_COLS].values
y_cls = df["risk_classification_enc"].values
y_reg = df["delivery_time_deviation"].values

log(f"  Features used ({len(FEATURE_COLS)}): {FEATURE_COLS}")
log()

# ─────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT
# ─────────────────────────────────────────────
X_train, X_test, yc_train, yc_test, yr_train, yr_test = train_test_split(
    X, y_cls, y_reg, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_cls
)
log(f"  Train: {len(X_train):,}  |  Test: {len(X_test):,}")
log()

# Shared scaler (used for linear models)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ─────────────────────────────────────────────
# 3. CLASSIFICATION
# ─────────────────────────────────────────────
log("=" * 65)
log("CLASSIFICATION  →  risk_classification")
log("=" * 65)

classifiers = {
    "Logistic Regression":      LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "Random Forest":            RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
    "Gradient Boosting":        GradientBoostingClassifier(n_estimators=200, random_state=RANDOM_STATE),
    "XGBoost":                  XGBClassifier(n_estimators=200, use_label_encoder=False,
                                              eval_metric="mlogloss", random_state=RANDOM_STATE,
                                              verbosity=0, n_jobs=-1),
    "LightGBM":                 lgb.LGBMClassifier(n_estimators=200, random_state=RANDOM_STATE,
                                                    n_jobs=-1, verbose=-1),
}

cls_results = {}
skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

for name, clf in classifiers.items():
    t0 = time.time()
    # Use scaled data for linear model, raw for tree models
    Xtr = X_train_sc if "Logistic" in name else X_train
    Xte = X_test_sc  if "Logistic" in name else X_test

    cv_scores = cross_val_score(clf, Xtr, yc_train, cv=skf, scoring="f1_macro", n_jobs=-1)
    clf.fit(Xtr, yc_train)
    preds = clf.predict(Xte)
    acc   = accuracy_score(yc_test, preds)
    f1    = f1_score(yc_test, preds, average="macro")
    elapsed = time.time() - t0

    cls_results[name] = {"model": clf, "acc": acc, "f1": f1,
                         "cv_mean": cv_scores.mean(), "cv_std": cv_scores.std(),
                         "preds": preds, "elapsed": elapsed}

    log(f"\n  [{name}]")
    log(f"    CV F1 (macro): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    log(f"    Test Accuracy: {acc:.4f}   Test F1 (macro): {f1:.4f}   Time: {elapsed:.1f}s")

# Pick best by test F1
best_cls_name = max(cls_results, key=lambda k: cls_results[k]["f1"])
best_cls      = cls_results[best_cls_name]
log()
log(f"  [OK] Best Classifier: {best_cls_name}  (F1={best_cls['f1']:.4f})")

log()
log(f"  Classification Report — {best_cls_name}:")
log(classification_report(yc_test, best_cls["preds"], target_names=class_names))

# Confusion matrix plot
cm = confusion_matrix(yc_test, best_cls["preds"])
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names, ax=ax)
ax.set_title(f"Confusion Matrix — {best_cls_name}")
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "confusion_matrix.png"), dpi=150)
plt.close()
log("  Saved: plots/confusion_matrix.png")

# Feature importance (tree models)
if hasattr(best_cls["model"], "feature_importances_"):
    fi = pd.Series(best_cls["model"].feature_importances_, index=FEATURE_COLS).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    fi.head(15).plot(kind="barh", ax=ax, color="steelblue")
    ax.set_title(f"Top 15 Feature Importances — {best_cls_name}")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "cls_feature_importance.png"), dpi=150)
    plt.close()
    log("  Saved: plots/cls_feature_importance.png")

# Save best classifier
cls_path = os.path.join(MODEL_DIR, "best_classifier.pkl")
with open(cls_path, "wb") as f:
    pickle.dump({"model": best_cls["model"], "label_encoder": le,
                 "scaler": scaler, "feature_cols": FEATURE_COLS,
                 "model_name": best_cls_name}, f)
log(f"  Saved: {cls_path}")

# ─────────────────────────────────────────────
# 4. REGRESSION
# ─────────────────────────────────────────────
log()
log("=" * 65)
log("REGRESSION  →  delivery_time_deviation")
log("=" * 65)

regressors = {
    "Ridge Regression":         Ridge(alpha=1.0),
    "Random Forest":            RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
    "Gradient Boosting":        GradientBoostingRegressor(n_estimators=200, random_state=RANDOM_STATE),
    "XGBoost":                  XGBRegressor(n_estimators=200, random_state=RANDOM_STATE,
                                             verbosity=0, n_jobs=-1),
    "LightGBM":                 lgb.LGBMRegressor(n_estimators=200, random_state=RANDOM_STATE,
                                                   n_jobs=-1, verbose=-1),
}

reg_results = {}
kf = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

for name, reg in regressors.items():
    t0 = time.time()
    Xtr = X_train_sc if "Ridge" in name else X_train
    Xte = X_test_sc  if "Ridge" in name else X_test

    cv_scores = cross_val_score(reg, Xtr, yr_train, cv=kf, scoring="r2", n_jobs=-1)
    reg.fit(Xtr, yr_train)
    preds = reg.predict(Xte)
    mae   = mean_absolute_error(yr_test, preds)
    rmse  = np.sqrt(mean_squared_error(yr_test, preds))
    r2    = r2_score(yr_test, preds)
    elapsed = time.time() - t0

    reg_results[name] = {"model": reg, "mae": mae, "rmse": rmse, "r2": r2,
                         "cv_mean": cv_scores.mean(), "cv_std": cv_scores.std(),
                         "preds": preds, "elapsed": elapsed}

    log(f"\n  [{name}]")
    log(f"    CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    log(f"    Test  MAE={mae:.4f}  RMSE={rmse:.4f}  R²={r2:.4f}   Time: {elapsed:.1f}s")

# Pick best by R²
best_reg_name = max(reg_results, key=lambda k: reg_results[k]["r2"])
best_reg      = reg_results[best_reg_name]
log()
log(f"  [OK] Best Regressor: {best_reg_name}  (R²={best_reg['r2']:.4f})")

# Actual vs Predicted scatter plot
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(yr_test, best_reg["preds"], alpha=0.3, s=5, color="teal")
mn, mx = yr_test.min(), yr_test.max()
ax.plot([mn, mx], [mn, mx], "r--", lw=1.5, label="Perfect fit")
ax.set_xlabel("Actual"); ax.set_ylabel("Predicted")
ax.set_title(f"Actual vs Predicted — {best_reg_name}")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "regression_actual_vs_pred.png"), dpi=150)
plt.close()
log("  Saved: plots/regression_actual_vs_pred.png")

# Feature importance
if hasattr(best_reg["model"], "feature_importances_"):
    fi = pd.Series(best_reg["model"].feature_importances_, index=FEATURE_COLS).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    fi.head(15).plot(kind="barh", ax=ax, color="darkorange")
    ax.set_title(f"Top 15 Feature Importances — {best_reg_name}")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "reg_feature_importance.png"), dpi=150)
    plt.close()
    log("  Saved: plots/reg_feature_importance.png")

# Save best regressor
reg_path = os.path.join(MODEL_DIR, "best_regressor.pkl")
with open(reg_path, "wb") as f:
    pickle.dump({"model": best_reg["model"], "scaler": scaler,
                 "feature_cols": FEATURE_COLS, "model_name": best_reg_name}, f)
log(f"  Saved: {reg_path}")

# ─────────────────────────────────────────────
# 5. COMPARISON SUMMARY
# ─────────────────────────────────────────────
log()
log("=" * 65)
log("SUMMARY")
log("=" * 65)
log()
log("  CLASSIFICATION COMPARISON:")
log(f"  {'Model':<25} {'CV F1':>8} {'Test Acc':>10} {'Test F1':>9}")
log(f"  {'-'*25} {'-'*8} {'-'*10} {'-'*9}")
for n, r in sorted(cls_results.items(), key=lambda x: x[1]["f1"], reverse=True):
    star = " ◄ BEST" if n == best_cls_name else ""
    log(f"  {n:<25} {r['cv_mean']:>8.4f} {r['acc']:>10.4f} {r['f1']:>9.4f}{star}")

log()
log("  REGRESSION COMPARISON:")
log(f"  {'Model':<25} {'CV R²':>8} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
log(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
for n, r in sorted(reg_results.items(), key=lambda x: x[1]["r2"], reverse=True):
    star = " ◄ BEST" if n == best_reg_name else ""
    log(f"  {n:<25} {r['cv_mean']:>8.4f} {r['mae']:>8.4f} {r['rmse']:>8.4f} {r['r2']:>8.4f}{star}")

# Save report
report_path = os.path.join(REPORT_DIR, "model_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))
log()
log(f"  Full report saved → {report_path}")
log()
log("  Done! Done!")
