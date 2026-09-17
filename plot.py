# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
from pathlib import Path
import csv
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "tide_quarrybay_2025.csv"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

def main():
    time_labels = []
    tide_heights = []
    with open(DATA_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
        print("CSV Header:", header)
        # 遍历每一天的一行
        for row in reader:
            if len(row) < 26:
                continue
            try:
                month = int(row[0])
                day = int(row[1])
                # row[2] ~ row[25] 对应 01点 ~ 24点
                for hour_idx in range(2, 26):
                    hour = hour_idx - 1
                    height_str = row[hour_idx].strip()
                    if height_str == "-9999":
                        continue
                    height = float(height_str)
                    time_str = f"2025-{month:02d}-{day:02d} {hour:02d}:00"
                    time_labels.append(time_str)
                    tide_heights.append(height)
            except (ValueError, IndexError):
                continue

    print(f"\nTotal valid data points: {len(time_labels)}")
    if len(time_labels) == 0:
        print("⚠️ No valid data found!")
        return

    print("First 10 records:")
    for i in range(min(10, len(time_labels))):
        print(time_labels[i], tide_heights[i])

    fig, ax = plt.subplots(figsize=(14,5))
    ax.plot(time_labels, tide_heights, color="#2a6f7f", linewidth=1.0)
    ax.set_title("2025 Hourly Predicted Tide Height at Quarry Bay, Hong Kong")
    ax.set_xlabel("Date & Hour")
    ax.set_ylabel("Tide Height (m)")
    ax.grid(alpha=0.2)
    # 每隔336个点显示一个x标签，防止文字挤爆
    ax.set_xticks(time_labels[::336])
    ax.tick_params(axis='x', rotation=45)

    img_path = OUT / "plot.png"
    plt.savefig(img_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved plot to {img_path}")

if __name__ == "__main__":
    main()
