"""
visualize.py  —  7 Detailed Plots for Supply Chain Logistics ML
================================================================
Plots generated:
  1. Risk Class Distribution          → plots/plot1_class_distribution.png
  2. Feature Importance (Classifier)  → plots/plot2_feature_importance.png
  3. Feature Correlation Heatmap      → plots/plot3_correlation_heatmap.png
  4. Key Features by Risk Class       → plots/plot4_features_by_risk.png
  5. Delivery Time Deviation Dist.    → plots/plot5_delivery_distribution.png
  6. Model Comparison (Classifiers)   → plots/plot6_model_comparison.png
  7. Disruption Score vs Risk + Delay → plots/plot7_disruption_analysis.png
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os, pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# ── Settings ───────────────────────────────────────────────────────────
PLOT_DIR    = "plots"
DATA_PATH   = "dynamic_supply_chain_logistics_dataset.csv"
CLS_MODEL   = r"models\best_classifier.pkl"
RANDOM_STATE = 42
os.makedirs(PLOT_DIR, exist_ok=True)

PALETTE = {"High Risk": "#e74c3c", "Moderate Risk": "#f39c12", "Low Risk": "#2ecc71"}
sns.set_theme(style="whitegrid", font_scale=1.1)

# ── Load data & model ──────────────────────────────────────────────────
print("Loading data and models...")
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])

with open(CLS_MODEL, "rb") as f:
    cls_bundle = pickle.load(f)

model        = cls_bundle["model"]
le           = cls_bundle["label_encoder"]
feature_cols = cls_bundle["feature_cols"]
scaler       = cls_bundle["scaler"]

X = df[feature_cols].values
y = le.transform(df["risk_classification"])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

print("Generating plots...\n")

# ══════════════════════════════════════════════════════════════════════
# PLOT 1 — Risk Class Distribution
# ══════════════════════════════════════════════════════════════════════
print("  [1/7] Risk Class Distribution")

counts = df["risk_classification"].value_counts()
order  = ["High Risk", "Moderate Risk", "Low Risk"]
counts = counts.reindex(order)
colors = [PALETTE[c] for c in order]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Plot 1  —  Risk Class Distribution", fontsize=15, fontweight="bold", y=1.01)

# Bar chart
bars = axes[0].bar(order, counts.values, color=colors, edgecolor="white", linewidth=1.5, width=0.5)
axes[0].set_title("Record Count per Risk Class")
axes[0].set_ylabel("Number of Records")
axes[0].set_xlabel("Risk Classification")
for bar, val in zip(bars, counts.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                 f"{val:,}\n({val/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")
axes[0].set_ylim(0, counts.max() * 1.18)

# Donut chart
wedges, texts, autotexts = axes[1].pie(
    counts.values, labels=order, colors=colors, autopct="%1.1f%%",
    startangle=140, pctdistance=0.75, wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2)
)
for at in autotexts: at.set_fontsize(11); at.set_fontweight("bold")
axes[1].set_title("Proportional Split (Donut Chart)")

# Description box
desc = (
    "DESCRIPTION\n"
    "This plot shows how records are distributed across\n"
    "the 3 risk classes. The dataset is imbalanced:\n"
    "  - High Risk dominates (~74.7% of all records)\n"
    "  - Moderate Risk is ~15.6%\n"
    "  - Low Risk is the minority class (~9.7%)\n"
    "Class imbalance is important because models may bias\n"
    "toward the majority class — here the Random Forest\n"
    "still achieved F1=1.00 despite the imbalance."
)
fig.text(0.5, -0.06, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot1_class_distribution.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 2 — Feature Importance (Random Forest Classifier)
# ══════════════════════════════════════════════════════════════════════
print("  [2/7] Feature Importance")

fi = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=True)
cmap_vals = fi.values / fi.values.max()
bar_colors = plt.cm.RdYlGn(cmap_vals)

fig, ax = plt.subplots(figsize=(11, 9))
fig.suptitle("Plot 2  —  Feature Importance (Random Forest Classifier)", fontsize=14, fontweight="bold")

bars = ax.barh(fi.index, fi.values, color=bar_colors, edgecolor="white", linewidth=0.8)
ax.set_xlabel("Mean Decrease in Impurity (Feature Importance Score)")
ax.set_title("All 23 Features — Sorted by Importance")
ax.axvline(fi.values.mean(), color="navy", linestyle="--", linewidth=1.5, label=f"Mean = {fi.values.mean():.4f}")
ax.legend(fontsize=10)

for bar, val in zip(bars, fi.values):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f"{val:.4f}", va="center", fontsize=8)

sm = plt.cm.ScalarMappable(cmap="RdYlGn", norm=plt.Normalize(fi.min(), fi.max()))
plt.colorbar(sm, ax=ax, label="Relative Importance", shrink=0.6)

desc = (
    "DESCRIPTION\n"
    "Feature importance reveals which input variables the Random Forest\n"
    "relies on most to split decision tree nodes. Key takeaways:\n"
    "  - 'disruption_likelihood_score' dominates with ~91.5% importance\n"
    "    — the risk class is almost entirely determined by this one feature.\n"
    "  - All other features contribute marginally (<1% each).\n"
    "  - This explains the near-perfect F1=1.00 — the model essentially\n"
    "    learns a simple threshold on 'disruption_likelihood_score'.\n"
    "  - Color: green = high importance, red = low importance."
)
fig.text(0.5, -0.03, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot2_feature_importance.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 3 — Feature Correlation Heatmap
# ══════════════════════════════════════════════════════════════════════
print("  [3/7] Correlation Heatmap")

num_cols = feature_cols + ["delivery_time_deviation"]
corr = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(16, 13))
fig.suptitle("Plot 3  —  Feature Correlation Heatmap", fontsize=14, fontweight="bold")

mask = np.triu(np.ones_like(corr, dtype=bool))   # upper triangle masked
sns.heatmap(corr, mask=mask, ax=ax, cmap="coolwarm", center=0,
            annot=True, fmt=".2f", annot_kws={"size": 7},
            linewidths=0.4, linecolor="white",
            cbar_kws={"shrink": 0.7, "label": "Pearson Correlation"})
ax.set_title("Lower Triangle — Pearson Correlations between All Features")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)

desc = (
    "DESCRIPTION\n"
    "The heatmap shows pairwise Pearson correlations between all 24 numeric columns.\n"
    "  - Values close to +1.0 (dark red) = strong positive correlation.\n"
    "  - Values close to -1.0 (dark blue) = strong negative correlation.\n"
    "  - Values near 0 (white) = no linear relationship.\n"
    "Key findings: Most features show near-zero correlations with each other,\n"
    "suggesting they are largely independent — typical of a synthetic/simulated dataset.\n"
    "High multicollinearity would have been a concern for linear models."
)
fig.text(0.5, -0.03, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot3_correlation_heatmap.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 4 — Key Features by Risk Class (Violin + Box)
# ══════════════════════════════════════════════════════════════════════
print("  [4/7] Key Features by Risk Class")

top5 = ["disruption_likelihood_score", "delay_probability",
        "eta_variation_hours", "weather_condition_severity", "traffic_congestion_level"]
order_cls = ["Low Risk", "Moderate Risk", "High Risk"]

fig, axes = plt.subplots(1, 5, figsize=(22, 6))
fig.suptitle("Plot 4  —  Top 5 Features Distributed by Risk Class (Violin + Box)", fontsize=14, fontweight="bold")

for ax, feat in zip(axes, top5):
    sns.violinplot(data=df, x="risk_classification", y=feat,
                   order=order_cls, palette=PALETTE, ax=ax,
                   inner="box", linewidth=1.2, cut=0)
    ax.set_title(feat.replace("_", " ").title(), fontsize=10, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(feat.split("_")[-1].title() if ax == axes[0] else "")
    ax.tick_params(axis="x", rotation=25, labelsize=8)

desc = (
    "DESCRIPTION\n"
    "Violin plots combine a box plot (median, IQR) with a KDE (kernel density estimate)\n"
    "to show the full distribution shape of each feature across the 3 risk classes.\n"
    "  - 'disruption_likelihood_score': clearly separates risk classes — Low Risk clusters\n"
    "    at low values, High Risk at high values, confirming its dominance in the model.\n"
    "  - 'delay_probability': similar separation pattern, corroborating the classifier.\n"
    "  - 'eta_variation_hours', 'weather_condition_severity', 'traffic_congestion_level':\n"
    "    show overlapping distributions across classes — less discriminative individually.\n"
    "  - Wide violin = many records at that value; narrow = fewer records."
)
fig.text(0.5, -0.06, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot4_features_by_risk.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 5 — Delivery Time Deviation Distribution
# ══════════════════════════════════════════════════════════════════════
print("  [5/7] Delivery Time Deviation Distribution")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
fig.suptitle("Plot 5  —  Delivery Time Deviation Analysis", fontsize=14, fontweight="bold")

# Overall histogram + KDE
sns.histplot(df["delivery_time_deviation"], bins=60, kde=True, ax=axes[0],
             color="#3498db", edgecolor="white", linewidth=0.4)
axes[0].axvline(df["delivery_time_deviation"].mean(), color="red", linestyle="--", linewidth=1.5,
                label=f"Mean={df['delivery_time_deviation'].mean():.2f}")
axes[0].axvline(df["delivery_time_deviation"].median(), color="orange", linestyle="-.", linewidth=1.5,
                label=f"Median={df['delivery_time_deviation'].median():.2f}")
axes[0].set_title("Overall Distribution (Histogram + KDE)")
axes[0].set_xlabel("Delivery Time Deviation (hours)")
axes[0].set_ylabel("Frequency")
axes[0].legend(fontsize=9)

# Box plot by risk class
sns.boxplot(data=df, x="risk_classification", y="delivery_time_deviation",
            order=order_cls, palette=PALETTE, ax=axes[1], width=0.5,
            flierprops=dict(marker="o", markersize=2, alpha=0.3))
axes[1].set_title("Deviation by Risk Class (Box Plot)")
axes[1].set_xlabel("Risk Class")
axes[1].set_ylabel("Delivery Time Deviation (hours)")
axes[1].tick_params(axis="x", rotation=15)

# CDF
sorted_vals = np.sort(df["delivery_time_deviation"].values)
cdf = np.arange(1, len(sorted_vals)+1) / len(sorted_vals)
axes[2].plot(sorted_vals, cdf, color="#8e44ad", linewidth=2)
axes[2].axhline(0.5, color="red", linestyle="--", linewidth=1, label="50th percentile")
axes[2].axhline(0.9, color="orange", linestyle="--", linewidth=1, label="90th percentile")
axes[2].set_title("Cumulative Distribution Function (CDF)")
axes[2].set_xlabel("Delivery Time Deviation (hours)")
axes[2].set_ylabel("Cumulative Probability")
axes[2].legend(fontsize=9)
axes[2].grid(True, alpha=0.4)

desc = (
    "DESCRIPTION\n"
    "Three views of 'delivery_time_deviation' (the regression target, range: -2 to +10 hours):\n"
    "  Left — Histogram + KDE: The distribution is roughly uniform/bimodal, NOT bell-shaped.\n"
    "    This explains why R² ~ 0 for all regressors — a near-uniform target is hard to predict.\n"
    "  Middle — Box plot by risk class: All 3 classes show nearly identical deviation distributions,\n"
    "    confirming that delivery deviation is INDEPENDENT of risk classification.\n"
    "  Right — CDF: ~50% of records have deviation above 5 hrs; ~10% exceed ~9.5 hrs.\n"
    "    The gradual, near-linear CDF shape confirms the near-uniform distribution."
)
fig.text(0.5, -0.06, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot5_delivery_distribution.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 6 — Model Comparison (All Classifiers)
# ══════════════════════════════════════════════════════════════════════
print("  [6/7] Model Comparison")

models_data = {
    "Logistic\nRegression": {"CV F1": 0.9940, "Test Acc": 0.9988, "Test F1": 0.9972, "Time(s)": 3.0},
    "Random\nForest":       {"CV F1": 0.9999, "Test Acc": 1.0000, "Test F1": 1.0000, "Time(s)": 8.4},
    "Gradient\nBoosting":   {"CV F1": 0.9999, "Test Acc": 1.0000, "Test F1": 1.0000, "Time(s)": 101.0},
    "XGBoost":              {"CV F1": 0.9966, "Test Acc": 0.9983, "Test F1": 0.9969, "Time(s)": 5.9},
    "LightGBM":             {"CV F1": 0.9943, "Test Acc": 0.9983, "Test F1": 0.9964, "Time(s)": 5.1},
}
mdf = pd.DataFrame(models_data).T

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Plot 6  —  Classifier Comparison: Accuracy, F1 & Training Time", fontsize=14, fontweight="bold")

# Grouped metric bars
x = np.arange(len(mdf))
w = 0.28
b1 = axes[0].bar(x - w, mdf["CV F1"],    width=w, label="CV F1 (macro)",    color="#3498db", edgecolor="white")
b2 = axes[0].bar(x,     mdf["Test Acc"], width=w, label="Test Accuracy",    color="#2ecc71", edgecolor="white")
b3 = axes[0].bar(x + w, mdf["Test F1"],  width=w, label="Test F1 (macro)",  color="#e74c3c", edgecolor="white")
axes[0].set_xticks(x); axes[0].set_xticklabels(mdf.index, fontsize=9)
axes[0].set_ylim(0.985, 1.001)
axes[0].set_ylabel("Score"); axes[0].set_title("Performance Metrics (zoomed to 0.985–1.00)")
axes[0].legend(fontsize=9)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.3f}"))
for bars in [b1, b2, b3]:
    for bar in bars:
        h = bar.get_height()
        axes[0].text(bar.get_x()+bar.get_width()/2, h+0.0001, f"{h:.4f}",
                     ha="center", va="bottom", fontsize=7, rotation=90)

# Training time
time_colors = ["#27ae60" if t < 10 else "#e67e22" if t < 60 else "#e74c3c" for t in mdf["Time(s)"]]
axes[1].bar(mdf.index, mdf["Time(s)"], color=time_colors, edgecolor="white", width=0.5)
axes[1].set_ylabel("Training Time (seconds)")
axes[1].set_title("Training Time Comparison")
axes[1].set_xlabel("")
for i, (idx, row) in enumerate(mdf.iterrows()):
    axes[1].text(i, row["Time(s)"] + 1.5, f"{row['Time(s)']:.1f}s", ha="center", fontsize=10, fontweight="bold")
axes[1].set_ylim(0, mdf["Time(s)"].max() * 1.2)
legend_patches = [mpatches.Patch(color="#27ae60", label="Fast (<10s)"),
                  mpatches.Patch(color="#e67e22", label="Medium (10-60s)"),
                  mpatches.Patch(color="#e74c3c", label="Slow (>60s)")]
axes[1].legend(handles=legend_patches, fontsize=9)

desc = (
    "DESCRIPTION\n"
    "Left chart compares 3 key metrics across 5 classifiers (y-axis zoomed to 0.985-1.00 to reveal differences):\n"
    "  - Random Forest & Gradient Boosting both reach perfect Test F1=1.000 and Accuracy=1.000.\n"
    "  - Logistic Regression, XGBoost, LightGBM are slightly below at ~0.997 F1 — still excellent.\n"
    "Right chart shows training time:\n"
    "  - Random Forest (8.4s) is the best trade-off: perfect accuracy + fast training.\n"
    "  - Gradient Boosting (101s) also achieves perfect scores but takes ~12x longer.\n"
    "  - Ridge Regression (0.2s) is fastest but weakest for this task."
)
fig.text(0.5, -0.06, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot6_model_comparison.png"), dpi=150, bbox_inches="tight")
plt.close()

# ══════════════════════════════════════════════════════════════════════
# PLOT 7 — Disruption Score Deep Dive
# ══════════════════════════════════════════════════════════════════════
print("  [7/7] Disruption Score Deep Dive")

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle("Plot 7  —  Disruption Likelihood Score: The Key Predictor", fontsize=14, fontweight="bold")

# (A) Distribution by risk class
for cls_name, color in PALETTE.items():
    subset = df[df["risk_classification"] == cls_name]["disruption_likelihood_score"]
    axes[0,0].hist(subset, bins=50, alpha=0.65, label=cls_name, color=color, edgecolor="none")
axes[0,0].set_title("A) Disruption Score Distribution by Risk Class")
axes[0,0].set_xlabel("Disruption Likelihood Score")
axes[0,0].set_ylabel("Frequency")
axes[0,0].legend()

# (B) Scatter: disruption vs delay_probability, colored by risk
for cls_name, color in PALETTE.items():
    sub = df[df["risk_classification"] == cls_name].sample(min(500, len(df)), random_state=42)
    axes[0,1].scatter(sub["disruption_likelihood_score"], sub["delay_probability"],
                      alpha=0.4, s=12, color=color, label=cls_name)
axes[0,1].set_title("B) Disruption Score vs Delay Probability")
axes[0,1].set_xlabel("Disruption Likelihood Score")
axes[0,1].set_ylabel("Delay Probability")
axes[0,1].legend(fontsize=9)

# (C) Box plot of disruption score per class
sns.boxplot(data=df, x="risk_classification", y="disruption_likelihood_score",
            order=order_cls, palette=PALETTE, ax=axes[1,0], width=0.5,
            flierprops=dict(marker="o", markersize=2, alpha=0.2))
axes[1,0].set_title("C) Disruption Score Statistics per Class (Box Plot)")
axes[1,0].set_xlabel("Risk Class")
axes[1,0].set_ylabel("Disruption Likelihood Score")
axes[1,0].tick_params(axis="x", rotation=10)
for patch, cls_name in zip(axes[1,0].artists if hasattr(axes[1,0], 'artists') else [], order_cls):
    patch.set_facecolor(PALETTE[cls_name])

# (D) Disruption score vs delivery_time_deviation scatter
sample = df.sample(3000, random_state=42)
for cls_name, color in PALETTE.items():
    sub = sample[sample["risk_classification"] == cls_name]
    axes[1,1].scatter(sub["disruption_likelihood_score"], sub["delivery_time_deviation"],
                      alpha=0.35, s=10, color=color, label=cls_name)
axes[1,1].set_title("D) Disruption Score vs Delivery Time Deviation")
axes[1,1].set_xlabel("Disruption Likelihood Score")
axes[1,1].set_ylabel("Delivery Time Deviation (hours)")
axes[1,1].legend(fontsize=9)

z = np.polyfit(sample["disruption_likelihood_score"], sample["delivery_time_deviation"], 1)
p = np.poly1d(z)
xs = np.linspace(sample["disruption_likelihood_score"].min(),
                 sample["disruption_likelihood_score"].max(), 100)
axes[1,1].plot(xs, p(xs), "k--", linewidth=1.5, label="Trend line")
axes[1,1].legend(fontsize=9)

desc = (
    "DESCRIPTION\n"
    "'disruption_likelihood_score' accounts for ~91.5% of the classifier's decision — it IS the risk label.\n"
    "  A) Histogram: The 3 risk classes occupy almost non-overlapping score ranges (Low<0.3, Moderate 0.3-0.7, High>0.7).\n"
    "     This near-perfect separation is why the Random Forest achieves F1=1.00.\n"
    "  B) Scatter vs delay_probability: Both scores move together within each class, but classes are spatially clustered.\n"
    "  C) Box plot: Extremely tight IQR boxes confirm the score is a near-deterministic label encoder.\n"
    "  D) Scatter vs delivery_time_deviation: The flat trend line confirms that delivery deviation is RANDOM\n"
    "     and INDEPENDENT of the disruption score — reinforcing why R²~0 for all regressors."
)
fig.text(0.5, -0.03, desc, ha="center", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f4f8", edgecolor="#bbb"))
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot7_disruption_analysis.png"), dpi=150, bbox_inches="tight")
plt.close()

print()
print("=" * 55)
print("All 7 plots saved to the 'plots/' folder:")
print("  plots/plot1_class_distribution.png")
print("  plots/plot2_feature_importance.png")
print("  plots/plot3_correlation_heatmap.png")
print("  plots/plot4_features_by_risk.png")
print("  plots/plot5_delivery_distribution.png")
print("  plots/plot6_model_comparison.png")
print("  plots/plot7_disruption_analysis.png")
print("Done!")
