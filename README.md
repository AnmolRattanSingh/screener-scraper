# Screener Scraper

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
