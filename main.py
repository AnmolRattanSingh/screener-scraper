import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time

with open("tickers.txt", "r") as f:
    tickers = [ticker.strip() for ticker in f.readlines()]

urls = []
missed = []

# chart api: https://www.screener.in/api/company/1275356/chart/?q=Price-DMA50-DMA200-Volume&days=365
# api company search: https://www.screener.in/api/company/search/?q={ticker}
# peers data api: https://www.screener.in/api/company/{take id from first obj returned in json in company search}/peers/

for ticker in tickers:
    urls.append(f"https://www.screener.in/company/{ticker}/")

def handle_response(response, ticker, type):
    if response.status_code == 429:
        print(f"Rate limit exceeded on {type}. Waiting 10 seconds ...")
        missed.append(ticker)
        time.sleep(10)
        return False
    elif response.status_code == 404:
        print(f"Failed to retrieve {ticker}. Req: {type} Error code: {response.status_code}")
        missed.append(ticker)
        return False
    elif response.status_code != 200:
        print(f"Failed to retrieve {ticker}. Req: {type} Unknown error: {response.status_code}")
        missed.append(ticker)
        return False
    return True

for i, url in enumerate(urls):
    # Send a GET request to the webpage
    response = requests.get(url)
    if not handle_response(response, tickers[i], "main"):
        continue

    # Parse the webpage content
    soup = BeautifulSoup(response.content, "html.parser")

    warehouse_id = ""
    # Extract the warehouse_id from the div
    company_info_div = soup.find("div", id="company-info")
    if company_info_div:
        warehouse_id = company_info_div.get("data-warehouse-id", "")
    
    if not warehouse_id:
        print(f"Warehouse ID not found for {tickers[i]}")
        missed.append(tickers[i])
        continue

    # Send a GET request to the peers api
    peers_response = requests.get(f"https://www.screener.in/api/company/{warehouse_id}/peers/")
    if not handle_response(peers_response, tickers[i], "peers"):
        continue

    time.sleep(1)

    # Create the output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Create an Excel writer object
    excel_filename = f"{output_dir}/{tickers[i]}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:

        # Extract and save the "tickers-ratios" list
        tickers_ratios = soup.find("ul", id="tickers-ratios")
        if tickers_ratios:
            items = []
            for li in tickers_ratios.find_all("li"):
                title = li.find("span", class_="name").get_text(strip=True)
                value = li.find("span", class_="value").get_text(strip=True)
                items.append({"Title": title, "Value": value})

            df_ratios = pd.DataFrame(items)
            df_ratios.to_excel(writer, sheet_name="tickers Ratios", index=False)

        # Find all sections with relevant data
        sections = soup.find_all("section", class_="card")

        for section in sections:
            section_id = section.get("id")

            # get peers data
            peers_html = peers_response.text

            # Parse the peers HTML table
            peers_soup = BeautifulSoup(peers_html, "html.parser")
            peers_table = peers_soup.find("table")
            if peers_table:
                df_peers = pd.read_html(StringIO(str(peers_table)))[0]
                df_peers.to_excel(writer, sheet_name="Peers", index=False)
            else:
                print("nope")

            table = section.find("table")
            if table:
                # Read the HTML table into a DataFrame
                df = pd.read_html(StringIO(str(table)))[0]

                # Save the DataFrame to an Excel sheet with the section ID as the sheet name
                sheet_name = section_id.replace(' ', '_').replace('/', '-')
                df.to_excel(writer, sheet_name=sheet_name, index=False)

# clear tickers.txt and add missed tickers
with open("tickers.txt", "w") as f:
    for ticker in missed:
        f.write(f"{ticker}\n")
