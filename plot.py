# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
from pathlib import Path
import csv
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "rainfall-daily.csv"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

def main():
    dates = []
    rainfall = []
    with open(DATA_FILE, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                year = int(row["Year"])
                month = int(row["Month"])
                day = int(row["Day"])
                rain = float(row["Daily Rainfall"])
                # 过滤无效值（-9999代表缺测）
                if rain > -9999:
                    dates.append(f"{year}-{month:02d}-{day:02d}")
                    rainfall.append(rain)
            except (ValueError, KeyError):
                continue

    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(dates, rainfall, color="#2a6f7f", linewidth=1.2)
    ax.set_title("Daily Rainfall at Hong Kong Observatory")
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Rainfall (mm)")
    ax.grid(alpha=0.2)
    # X轴标签太多，隐藏一部分防止重叠
    ax.set_xticks(dates[::120])

    img_path = OUT / "plot.png"
    plt.savefig(img_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved plot to {img_path}")

if __name__ == "__main__":
    main()
