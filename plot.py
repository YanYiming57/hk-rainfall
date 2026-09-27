# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
from pathlib import Path
import csv
import matplotlib.pyplot as plt
from datetime import datetime

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "rainfall.csv"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

def main():
    all_rows = []
    with open(DATA_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            if len(row) < 4:
                continue
            try:
                year = int(row[0])
                month = int(row[1])
                day = int(row[2])
                rain_val = float(row[3])
                dt = datetime(year, month, day)
                all_rows.append([dt, rain_val])
            except ValueError:
                continue

    # 取最后24条，2026最新数据
    recent_24 = all_rows[-24:]
    date_list = [item[0] for item in recent_24]
    rainfall_mm = [item[1] for item in recent_24]

    print(f"Total valid data points: {len(date_list)}")
    start_date = date_list[0].strftime("%Y-%m-%d")
    end_date = date_list[-1].strftime("%Y-%m-%d")
    print(f"✅ NEW DATA RANGE: {start_date} to {end_date}")

    fig, ax = plt.subplots(figsize=(12, 6))
    # 颜色设置：米黄色背景 + 全套绿色
    bg_color = "#fbf0d9"
    line_color = "#0f5132"
    fill_color = "#2da44e"
    highlight_green = "#1f7f3f"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.plot(date_list, rainfall_mm, color=line_color, linewidth=2.5, marker="o", markersize=5)
    ax.fill_between(date_list, rainfall_mm, color=fill_color, alpha=0.22)

    idx_high = rainfall_mm.index(max(rainfall_mm))
    idx_low = rainfall_mm.index(min(rainfall_mm))
    max_day_idx = len(date_list)-1

    # -------- 最高值标注 --------
    ax.scatter(date_list[idx_high], rainfall_mm[idx_high], color=highlight_green, s=110, zorder=5)
    if idx_high > max_day_idx * 0.85:
        dx_high = -0.35
    else:
        dx_high = 0.25
    dy_high = 0.04 * max(rainfall_mm)
    ax.text(date_list[idx_high], rainfall_mm[idx_high] + dy_high,
            f"{rainfall_mm[idx_high]:.1f} mm",
            color=highlight_green, fontsize=11, fontweight="bold")

    # -------- 最低值标注（文字向上，不会跑出图框） --------
    ax.scatter(date_list[idx_low], rainfall_mm[idx_low], color=highlight_green, s=110, zorder=5)
    if idx_low < max_day_idx * 0.15:
        dx_low = 0.25
    elif idx_low > max_day_idx * 0.85:
        dx_low = -0.35
    else:
        dx_low = 0.25
    dy_low = 0.04 * max(rainfall_mm)
    ax.text(date_list[idx_low], rainfall_mm[idx_low] + dy_low,
            f"{rainfall_mm[idx_low]:.1f} mm",
            color=highlight_green, fontsize=11, fontweight="bold")

    ax.set_title(f"Daily Rainfall at HKO — {start_date} to {end_date}", fontsize=16, pad=15)
    ax.set_xlabel("Date", fontsize=13)
    ax.set_ylabel("rainfall (mm)", fontsize=13)
    ax.grid(alpha=0.3)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.margins(x=0, y=0)
    ax.set_ylim(bottom=ax.get_ylim()[0], top=ax.get_ylim()[1] * 1.12)

    img_path = OUT / "plot.png"
    plt.tight_layout()
    plt.savefig(img_path, dpi=150)
    plt.show()
    print("✅ New green chart saved with latest 2026 rainfall data!")

if __name__ == "__main__":
    main()
