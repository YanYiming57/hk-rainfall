# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
from pathlib import Path
import requests

HERE = Path(__file__).parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

# 2025 Quarry Bay hourly astronomical tide data (HKO open API)
URL = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=HHOT&station=QUB&year=2025&rformat=csv"
FILE = DATA / "tide_quarrybay_2025.csv"

def main():
    if FILE.exists():
        print(f"{FILE.name} already exists, skip download.")
        return
    print(f"Downloading tide data ...")
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    FILE.write_bytes(resp.content)
    print(f"Saved to {FILE}")

if __name__ == "__main__":
    main()
