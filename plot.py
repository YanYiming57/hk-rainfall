# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
from pathlib import Path
import csv
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "rainfall.csv"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

def main():
    day_labels = []
    rainfall_mm = []

    with open(DATA_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            if len(row) < 4:
                continue
            try:
                # HKO CSV: col0=year, col1=month, col2=day, col3=total rainfall
                rain_val = float(row[3])
                day_labels.append(len(day_labels)+1)
                rainfall_mm.append(rain_val)
                # collect 24 valid points then stop
                if len(rainfall_mm) >= 24:
                    break
            except ValueError:
                # skip row if value cannot convert to number
                continue

    print(f"Total valid data points: {len(rainfall_mm)}")

    fig, ax = plt.subplots(figsize=(12, 6))
    # warm colour palette
    bg_color = "#fbf0d9"
    line_color = "#7a0101"
    fill_color = "#be1420"
    highlight_red = "#be1420"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.plot(day_labels, rainfall_mm, color=line_color, linewidth=2.5, marker="o", markersize=5)
    ax.fill_between(day_labels, rainfall_mm, color=fill_color, alpha=0.22)

    idx_high = rainfall_mm.index(max(rainfall_mm))
    idx_low = rainfall_mm.index(min(rainfall_mm))
    max_day = max(day_labels)

    # -------- 最高值标注 --------
    ax.scatter(day_labels[idx_high], rainfall_mm[idx_high], color=highlight_red, s=110, zorder=5)
    if day_labels[idx_high] > max_day * 0.85:
        dx_high = -0.4
    else:
        dx_high = 0.25
    dy_high = 0.04 * max(rainfall_mm)
    ax.text(day_labels[idx_high] + dx_high, rainfall_mm[idx_high] + dy_high,
            f"{rainfall_mm[idx_high]:.1f} mm",
            color=highlight_red, fontsize=11, fontweight="bold")

    # -------- 最低值标注【重点修改】 --------
    ax.scatter(day_labels[idx_low], rainfall_mm[idx_low], color=highlight_red, s=110, zorder=5)
    # 最低点文字放在点的上方，不再往下！
    if day_labels[idx_low] < max_day * 0.15:
        dx_low = 0.25
    elif day_labels[idx_low] > max_day * 0.85:
        dx_low = -0.4
    else:
        dx_low = 0.25
    dy_low = 0.04 * max(rainfall_mm) # 向上偏移！
    ax.text(day_labels[idx_low] + dx_low, rainfall_mm[idx_low] + dy_low,
            f"{rainfall_mm[idx_low]:.1f} mm",
            color=highlight_red, fontsize=11, fontweight="bold")

    ax.set_title("Daily Rainfall at HKO — 24 consecutive days", fontsize=16, pad=15)
    ax.set_xlabel("day", fontsize=13)
    ax.set_ylabel("rainfall (mm)", fontsize=13)
    ax.grid(alpha=0.3)
    ax.set_xticks(day_labels)
    ax.margins(x=0, y=0)
    ax.set_ylim(bottom=ax.get_ylim()[0], top=ax.get_ylim()[1] * 1.12)

    img_path = OUT / "plot.png"
    plt.tight_layout()
    plt.savefig(img_path, dpi=150)
    plt.show()
    print("Plot saved successfully!")

if __name__ == "__main__":
    main()
