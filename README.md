# Screener Scraper

## Disclaimer

This project is not affiliated with, endorsed by, or in any way officially connected to [Screener](https://www.screener.in/). The data is sourced from [Screener](https://www.screener.in/) and users must comply with their [terms of service](https://www.screener.in/guides/terms/). This project is intended solely for personal or educational use to aid in data analysis. It is important to respect Screener's intellectual property and usage policies when using this project.

## How to use

Scrape data from [Screener](https://www.screener.in/) and save it to an Excel file. The data is saved to the `output` folder. Enter the ticker symbols in the `tickers.txt` file separated by newlines. Then run `python3 main.py` to compare the data in the `output` folder with the data in the `tickers.txt` file.

## Extracting Peers

Incase you want to extract the "Peers" sheet from the Excel files in the `output` folder, run the following command:

```bash
python3 extract_peers.py
```

## Install dependencies

```bash
pip install -r requirements.txt
```
