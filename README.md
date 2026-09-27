# rainfall
This repository visualises 24 consecutive days of daily total rainfall measurements recorded at Hong Kong Observatory. This project transforms raw weather numerical data into a static visualisation for the week 03 assignment: Numbers into pictures.

## Project Overview
The dataset is official daily rainfall records from the Hong Kong Observatory. The line chart shows how daily rainfall changes across 24 days. Each red dot represents the total rainfall (mm) for one day. The maximum and minimum rainfall values are annotated on the graph, with text positions automatically adjusted to ensure all labels stay within the plot boundary. The chart uses a warm red colour scheme with a cream background.

## Repository Structure
├── fetch.py        # Script to download official rainfall CSV data
├── plot.py         # Script to read local CSV and generate the rainfall chart
├── README.md       # Project description
├── PROCESS.md      # Development process notes
├── data/
│   └── rainfall.csv  # Saved local rainfall dataset (committed to repo, works offline)
└── out/
└── plot.png    # Output visualisation image
## How to run
1. Clone this repository
2. Run `uv run fetch.py` to download the official rainfall dataset
3. Run `uv run plot.py` to generate and open the rainfall chart, the output image will save to `out/plot.png`

All raw data files are stored inside this repository. The visualisation can work without internet after the first data download.
