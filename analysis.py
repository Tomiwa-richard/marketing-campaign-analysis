"""Reproducible customer and marketing campaign analysis.

Expected input: marketing_campaign.xlsx, with the original customer campaign
columns. Run from the repository root with: python analysis.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent

PRODUCT_COLUMNS = [
    "MntWines",
    "MntMeatProducts",
    "MntGoldProds",
    "MntFishProducts",
    "MntSweetProducts",
    "MntFruits",
]
PRODUCT_LABELS = {
    "MntWines": "Wine",
    "MntMeatProducts": "Meat",
    "MntGoldProds": "Gold",
    "MntFishProducts": "Fish",
    "MntSweetProducts": "Sweets",
    "MntFruits": "Fruits",
}
CHANNEL_COLUMNS = [
    "NumStorePurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumDealsPurchases",
]
CHANNEL_LABELS = {
    "NumStorePurchases": "Store",
    "NumWebPurchases": "Web",
    "NumCatalogPurchases": "Catalog",
    "NumDealsPurchases": "Deals",
}
CAMPAIGN_COLUMNS = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response",
]
CAMPAIGN_LABELS = {
    "AcceptedCmp1": "Campaign 1",
    "AcceptedCmp2": "Campaign 2",
    "AcceptedCmp3": "Campaign 3",
    "AcceptedCmp4": "Campaign 4",
    "AcceptedCmp5": "Campaign 5",
    "Response": "Last campaign",
}


def load_and_clean_data(path: Path) -> pd.DataFrame:
    """Load the source workbook, apply the documented cleaning, and engineer features."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Place marketing_campaign.xlsx in the data/ folder, or pass --data PATH."
        )

    df = pd.read_excel(path)
    required = {
        "Year_Birth", "Income", "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumWebPurchases",
        "NumCatalogPurchases", "NumStorePurchases", "NumDealsPurchases",
        *CAMPAIGN_COLUMNS,
    }
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Workbook is missing required columns: {', '.join(missing)}")

    # Remove missing income, known invalid birth-year and income records.
    df = df.dropna(subset=["Income"]).copy()
    df = df.loc[df["Year_Birth"].ne(1893) & df["Income"].lt(600_000)].copy()
    df = df.drop(columns=["Z_CostContact", "Z_Revenue"], errors="ignore")

    # The source notebook uses 2015 as the reference year; remove implausible ages.
    df["Age"] = 2015 - df["Year_Birth"]
    df = df.loc[df["Age"].lt(100)].copy()

    df["TotalSpend"] = df[PRODUCT_COLUMNS].sum(axis=1)
    df["TotalPurchases"] = df[["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]].sum(axis=1)
    df["FamilySize"] = df["Kidhome"] + df["Teenhome"] if {"Kidhome", "Teenhome"}.issubset(df.columns) else np.nan
    df["HasChildren"] = (df["FamilySize"].fillna(0) > 0).astype(int)
    df["AcceptedAnyCampaign"] = df[[c for c in CAMPAIGN_COLUMNS[:-1] if c in df]].max(axis=1)
    return df


def save_charts(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=1.0)
    color = "#4263EB"

    product_spend = df[PRODUCT_COLUMNS].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    sns.barplot(x=[PRODUCT_LABELS[c] for c in product_spend.index], y=product_spend.values,
                color=color, ax=ax)
    ax.set(title="Average Spend by Product Category", xlabel="Product category", ylabel="Average spend ($)")
    fig.tight_layout()
    fig.savefig(output_dir / "product_spend.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    channel_purchases = df[CHANNEL_COLUMNS].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    sns.barplot(x=[CHANNEL_LABELS[c] for c in channel_purchases.index], y=channel_purchases.values,
                color=color, ax=ax)
    ax.set(title="Average Purchases by Channel", xlabel="Channel", ylabel="Purchases per customer")
    fig.tight_layout()
    fig.savefig(output_dir / "purchase_channels.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    acceptance = df[CAMPAIGN_COLUMNS].mean().mul(100)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    sns.barplot(x=[CAMPAIGN_LABELS[c] for c in acceptance.index], y=acceptance.values,
                color=color, ax=ax)
    ax.set(title="Campaign Acceptance Rates", xlabel="Campaign", ylabel="Customers accepting (%)")
    ax.tick_params(axis="x", rotation=12)
    fig.tight_layout()
    fig.savefig(output_dir / "campaign_acceptance.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def print_summary(df: pd.DataFrame) -> None:
    product_spend = df[PRODUCT_COLUMNS].mean().sort_values(ascending=False)
    channels = df[CHANNEL_COLUMNS].mean().sort_values(ascending=False)
    acceptance = df[CAMPAIGN_COLUMNS].mean().mul(100).sort_values(ascending=False)

    print("\nMARKETING CAMPAIGN ANALYSIS")
    print("=" * 30)
    print(f"Customers analyzed: {len(df):,}")
    print(f"Average income: ${df['Income'].mean():,.2f}")
    print(f"Average age: {df['Age'].mean():.1f}")
    print(f"Income / total-spend correlation: {df['Income'].corr(df['TotalSpend']):.2f}")
    print(f"Highest average product spend: {PRODUCT_LABELS[product_spend.index[0]]} (${product_spend.iloc[0]:,.2f})")
    print(f"Most-used purchase channel: {CHANNEL_LABELS[channels.index[0]]} ({channels.iloc[0]:.2f} avg purchases)")
    print(f"Highest campaign acceptance: {CAMPAIGN_LABELS[acceptance.index[0]]} ({acceptance.iloc[0]:.2f}%)")
    print("\nCharts saved to the images/ directory.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "marketing_campaign.xlsx",
                        help="Path to the source Excel workbook")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "images",
                        help="Directory for generated charts")
    args = parser.parse_args()

    df = load_and_clean_data(args.data)
    print_summary(df)
    save_charts(df, args.output_dir)


if __name__ == "__main__":
    main()
