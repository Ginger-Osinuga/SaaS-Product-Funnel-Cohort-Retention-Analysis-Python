# =============================================================================
# PROJECT 1: SaaS Funnel and Cohort Retention Analysis
# =============================================================================
# What this project does:
#   - Simulates a real product-led growth (PLG) funnel: Visited > Signed Up >
#     Activated > Converted to Paid
#   - Calculates conversion rates at each stage
#   - Analyzes cohort retention (how many users are still active after 30, 60,
#     90 days) broken out by acquisition channel
#   - Produces publication-quality charts saved as PNG files
#
# Why this matters for product analytics roles:
#   Funnel analysis and cohort retention are two of the most common daily tasks
#   for a product data analyst. This project demonstrates both skills.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime, timedelta
import random
import os

# Set a random seed so results are reproducible every time you run this
np.random.seed(42)
random.seed(42)

# Create output folder for charts
os.makedirs("outputs", exist_ok=True)

print("=" * 60)
print("PROJECT 1: SaaS Funnel and Cohort Retention Analysis")
print("=" * 60)


# -----------------------------------------------------------------------------
# STEP 1: Generate synthetic user data
# -----------------------------------------------------------------------------
# We create 5,000 simulated users who visited our SaaS product over 6 months.
# Each user has a signup date, acquisition channel, and flags for whether they
# completed each stage of the funnel.

NUM_USERS = 5000
CHANNELS  = ["Organic Search", "Paid Social", "Email Campaign", "Referral", "Direct"]

# Signup dates spread across 6 months
start_date = datetime(2024, 1, 1)
signup_dates = [start_date + timedelta(days=random.randint(0, 180))
                for _ in range(NUM_USERS)]

# Acquisition channel (weighted so Organic is most common)
channels = random.choices(
    CHANNELS,
    weights=[0.35, 0.20, 0.18, 0.15, 0.12],
    k=NUM_USERS
)

# Funnel conversion probabilities per channel
# Each number = probability a user from that channel reaches the next stage
channel_conversion = {
    #                signup   activate  paid
    "Organic Search":  [0.52,   0.41,   0.22],
    "Paid Social":     [0.38,   0.28,   0.14],
    "Email Campaign":  [0.61,   0.50,   0.28],
    "Referral":        [0.70,   0.62,   0.38],
    "Direct":          [0.55,   0.44,   0.24],
}

rows = []
for i in range(NUM_USERS):
    ch = channels[i]
    p_signup, p_activate, p_paid = channel_conversion[ch]

    visited   = 1
    signed_up = 1 if random.random() < p_signup   else 0
    activated = 1 if signed_up and random.random() < p_activate else 0
    paid      = 1 if activated and random.random() < p_paid     else 0

    # Days until each stage (realistic delays)
    days_to_activate = random.randint(0, 3)  if activated else None
    days_to_paid     = random.randint(1, 14) if paid      else None

    rows.append({
        "user_id":        f"U{i+1:05d}",
        "signup_date":    signup_dates[i],
        "channel":        ch,
        "visited":        visited,
        "signed_up":      signed_up,
        "activated":      activated,
        "converted_paid": paid,
        "days_to_activate": days_to_activate,
        "days_to_paid":     days_to_paid,
    })

df = pd.DataFrame(rows)

print(f"\nDataset created: {len(df):,} users")
print(f"Date range: {df['signup_date'].min().date()} to {df['signup_date'].max().date()}")


# -----------------------------------------------------------------------------
# STEP 2: Overall funnel analysis
# -----------------------------------------------------------------------------

print("\n--- OVERALL FUNNEL ---")

funnel_stages = {
    "Visited Site":    df["visited"].sum(),
    "Signed Up":       df["signed_up"].sum(),
    "Activated":       df["activated"].sum(),
    "Converted Paid":  df["converted_paid"].sum(),
}

# Calculate conversion rates between each stage
stage_names  = list(funnel_stages.keys())
stage_counts = list(funnel_stages.values())

print(f"\n{'Stage':<20} {'Users':>8} {'Conv from prev':>16} {'Conv from top':>16}")
print("-" * 64)
for i, (stage, count) in enumerate(funnel_stages.items()):
    from_prev = f"{count/stage_counts[i-1]*100:.1f}%" if i > 0 else "---"
    from_top  = f"{count/stage_counts[0]*100:.1f}%"
    print(f"{stage:<20} {count:>8,} {from_prev:>16} {from_top:>16}")


# -----------------------------------------------------------------------------
# STEP 3: Funnel chart
# -----------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))

colors = ["#2563A8", "#3B7DD8", "#6FA3E8", "#A8C8F0"]
bars   = ax.barh(stage_names[::-1], stage_counts[::-1], color=colors, height=0.55)

# Add count and percentage labels inside bars
for i, (bar, count) in enumerate(zip(bars, stage_counts[::-1])):
    pct = count / stage_counts[0] * 100
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height() / 2,
            f"{count:,}  ({pct:.1f}%)",
            va="center", ha="left", fontsize=11, color="#333333")

ax.set_xlabel("Number of Users", fontsize=12)
ax.set_title("SaaS Product Funnel: Visitor to Paid Conversion", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xlim(0, stage_counts[0] * 1.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/01_funnel_overall.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart saved: outputs/01_funnel_overall.png")


# -----------------------------------------------------------------------------
# STEP 4: Funnel by acquisition channel
# -----------------------------------------------------------------------------

print("\n--- PAID CONVERSION RATE BY CHANNEL ---")

channel_summary = (
    df.groupby("channel")
      .agg(
          total_users      = ("visited",        "sum"),
          signed_up        = ("signed_up",       "sum"),
          activated        = ("activated",       "sum"),
          converted_paid   = ("converted_paid",  "sum"),
      )
      .assign(paid_conversion_rate = lambda x: x["converted_paid"] / x["total_users"] * 100)
      .sort_values("paid_conversion_rate", ascending=False)
)

print(channel_summary[["total_users", "signed_up", "activated",
                         "converted_paid", "paid_conversion_rate"]].to_string())

fig, ax = plt.subplots(figsize=(10, 5))
ch_sorted = channel_summary.sort_values("paid_conversion_rate")
bar_colors = ["#A8C8F0" if v < channel_summary["paid_conversion_rate"].mean()
              else "#2563A8" for v in ch_sorted["paid_conversion_rate"]]
bars = ax.barh(ch_sorted.index, ch_sorted["paid_conversion_rate"], color=bar_colors, height=0.5)

for bar, val in zip(bars, ch_sorted["paid_conversion_rate"]):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=11)

mean_rate = channel_summary["paid_conversion_rate"].mean()
ax.axvline(mean_rate, color="#E05C2A", linestyle="--", linewidth=1.5, label=f"Average: {mean_rate:.1f}%")
ax.legend(fontsize=10)
ax.set_xlabel("Paid Conversion Rate (%)", fontsize=12)
ax.set_title("Paid Conversion Rate by Acquisition Channel", fontsize=14, fontweight="bold", pad=15)
ax.set_xlim(0, ch_sorted["paid_conversion_rate"].max() * 1.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/02_conversion_by_channel.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart saved: outputs/02_conversion_by_channel.png")


# -----------------------------------------------------------------------------
# STEP 5: Cohort retention analysis
# -----------------------------------------------------------------------------
# For each monthly signup cohort, track what % of activated users are still
# "active" at 30, 60, and 90 days (simulated with realistic decay curves).

print("\n--- COHORT RETENTION ANALYSIS ---")

# Only look at activated users
activated_users = df[df["activated"] == 1].copy()
activated_users["cohort_month"] = activated_users["signup_date"].dt.to_period("M")

# Simulate retention: users have a random "active until" date
def simulate_retention_days(channel):
    # Referral users retain best; Paid Social worst
    mean_days = {
        "Referral": 95, "Email Campaign": 80, "Organic Search": 72,
        "Direct": 68,   "Paid Social": 55
    }
    return max(0, int(np.random.exponential(scale=mean_days.get(channel, 70))))

activated_users["active_days"] = activated_users["channel"].apply(simulate_retention_days)
activated_users["retained_30"]  = (activated_users["active_days"] >= 30).astype(int)
activated_users["retained_60"]  = (activated_users["active_days"] >= 60).astype(int)
activated_users["retained_90"]  = (activated_users["active_days"] >= 90).astype(int)

cohort_retention = (
    activated_users.groupby("cohort_month")
    .agg(
        cohort_size   = ("user_id",      "count"),
        retained_d30  = ("retained_30",  "mean"),
        retained_d60  = ("retained_60",  "mean"),
        retained_d90  = ("retained_90",  "mean"),
    )
    .reset_index()
)
cohort_retention["cohort_month"] = cohort_retention["cohort_month"].astype(str)

print("\nCohort Retention Table (% of activated users still active):")
display_cols = cohort_retention.copy()
for col in ["retained_d30", "retained_d60", "retained_d90"]:
    display_cols[col] = display_cols[col].map("{:.1%}".format)
print(display_cols.to_string(index=False))

# Heatmap
fig, ax = plt.subplots(figsize=(9, 5))
heat_data = cohort_retention.set_index("cohort_month")[["retained_d30", "retained_d60", "retained_d90"]]
heat_data.columns = ["Day 30", "Day 60", "Day 90"]
heat_data = heat_data * 100  # convert to percentage

sns.heatmap(
    heat_data, annot=True, fmt=".1f", cmap="Blues",
    linewidths=0.5, linecolor="white",
    cbar_kws={"label": "Retention Rate (%)"},
    ax=ax
)
ax.set_title("Cohort Retention Heatmap (% Active at 30 / 60 / 90 Days)", fontsize=13, fontweight="bold", pad=15)
ax.set_ylabel("Signup Cohort (Month)", fontsize=11)
ax.set_xlabel("Days Since Activation", fontsize=11)
plt.tight_layout()
plt.savefig("outputs/03_cohort_retention_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart saved: outputs/03_cohort_retention_heatmap.png")


# -----------------------------------------------------------------------------
# STEP 6: Save clean datasets for inspection
# -----------------------------------------------------------------------------

df.to_csv("outputs/user_funnel_data.csv", index=False)
channel_summary.to_csv("outputs/channel_summary.csv")
cohort_retention.to_csv("outputs/cohort_retention.csv", index=False)

print("\n" + "=" * 60)
print("All outputs saved to the 'outputs/' folder.")
print("Files created:")
print("  - outputs/01_funnel_overall.png")
print("  - outputs/02_conversion_by_channel.png")
print("  - outputs/03_cohort_retention_heatmap.png")
print("  - outputs/user_funnel_data.csv")
print("  - outputs/channel_summary.csv")
print("  - outputs/cohort_retention.csv")
print("=" * 60)
