# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
from pathlib import Path
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

    # 取最近60条（两个月数据）
    recent_60 = all_rows[-60:]
    date_list = [item[0] for item in recent_60]
    rainfall_mm = [item[1] for item in recent_60]

    print(f"Total valid data points: {len(date_list)}")
    start_date = date_list[0].strftime("%Y-%m-%d")
    end_date = date_list[-1].strftime("%Y-%m-%d")
    print(f"✅ Data range (latest 2 months): {start_date} to {end_date}")

    fig, ax = plt.subplots(figsize=(14, 6))
    # 颜色：绿色线条填充，极值点深红色
    bg_color = "#fbf0d9"
    line_color = "#0f5132"
    fill_color = "#2da44e"
    highlight_red = "#a80000"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.plot(date_list, rainfall_mm, color=line_color, linewidth=2.0, marker="o", markersize=4)
    ax.fill_between(date_list, rainfall_mm, color=fill_color, alpha=0.22)

    idx_high = rainfall_mm.index(max(rainfall_mm))
    idx_low = rainfall_mm.index(min(rainfall_mm))

    # 最高值标注（深红色）
    ax.scatter(date_list[idx_high], rainfall_mm[idx_high], color=highlight_red, s=110, zorder=5)
    dy_high = 0.04 * max(rainfall_mm)
    ax.text(date_list[idx_high], rainfall_mm[idx_high] + dy_high,
            f"{rainfall_mm[idx_high]:.1f} mm",
            color=highlight_red, fontsize=10, fontweight="bold")

    # 最低值标注（深红色）
    ax.scatter(date_list[idx_low], rainfall_mm[idx_low], color=highlight_red, s=110, zorder=5)
    dy_low = 0.04 * max(rainfall_mm)
    ax.text(date_list[idx_low], rainfall_mm[idx_low] + dy_low,
            f"{rainfall_mm[idx_low]:.1f} mm",
            color=highlight_red, fontsize=10, fontweight="bold")

    ax.set_title("Daily rain at HKO", fontsize=16, pad=15)
    ax.set_xlabel(f"Date | {start_date} to {end_date}", fontsize=13)
    ax.set_ylabel("rainfall (mm)", fontsize=13)

    # X轴日期定位：主刻度7天，次刻度每一天
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    # 网格：主网格粗，次网格细
    ax.grid(True, which="major", alpha=0.4, linestyle="-", linewidth=1.0)
    ax.grid(True, which="minor", alpha=0.2, linestyle="-", linewidth=0.4)

    # ✅ 重点：X轴刻度短竖线（tick）粗细设置
    ax.tick_params(axis='x', which='major', length=8, width=2)   # 主刻度短竖线：更长、加粗
    ax.tick_params(axis='x', which='minor', length=4, width=0.8)# 次刻度短竖线：短、细
    ax.tick_params(axis='y', which='both', length=4, width=0.8) # Y轴保持正常

    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    ax.margins(x=0, y=0)
    ax.set_ylim(bottom=ax.get_ylim()[0], top=ax.get_ylim()[1] * 1.12)

    img_path = OUT / "plot.png"
    plt.tight_layout()
    plt.savefig(img_path, dpi=150)
    plt.show()
    print("✅ Chart saved, x-axis major tick marks (short vertical lines) are thickened.")

if __name__ == "__main__":
    main()
