# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
Download daily rainfall data from Hong Kong Observatory.
Save to data/rainfall.csv
"""
from pathlib import Path
import requests

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"
DATA_DIR.mkdir(exist_ok=True)
OUT_FILE = DATA_DIR / "rainfall.csv"
URL = "https://data.weather.gov.hk/weatherAPI/cis/csvfile/HKO/ALL/daily_HKO_RF_ALL.csv"

def main():
    print("Downloading rainfall data ...")
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    OUT_FILE.write_text(resp.text, encoding="utf-8-sig")
    print(f"Saved to {OUT_FILE}")

if __name__ == "__main__":
    main()
