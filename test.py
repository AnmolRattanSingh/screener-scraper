import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

with open("top.txt", "r") as f:
    tickers = [ticker.strip() for ticker in f.readlines()]

urls = []

for ticker in tickers:
    urls.append(f"https://www.screener.in/company/{ticker}/#quarters")

for i, url in enumerate(urls):
    # Send a GET request to the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {tickers[i]}")
        continue

    # Parse the webpage content
    soup = BeautifulSoup(response.content, "html.parser")

    # Create the output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Create an Excel writer object
    excel_filename = f"{output_dir}/{tickers[i]}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:

        # Extract and save the "top-ratios" list
        top_ratios = soup.find("ul", id="top-ratios")
        if top_ratios:
            items = []
            for li in top_ratios.find_all("li"):
                title = li.find("span", class_="name").get_text(strip=True)
                value = li.find("span", class_="value").get_text(strip=True)
                items.append({"Title": title, "Value": value})

            df_ratios = pd.DataFrame(items)
            df_ratios.to_excel(writer, sheet_name="Top Ratios", index=False)

        # Find all sections with relevant data
        sections = soup.find_all("section", class_="card")

        # Extract data from each section and save it to a CSV file
        for section in sections:
            section_id = section.get("id")
            table = section.find("table")
            if table:
                # Read the HTML table into a DataFrame
                df = pd.read_html(StringIO(str(table)))[0]

                # Save the DataFrame to an Excel sheet with the section ID as the sheet name
                sheet_name = section_id.replace(' ', '_').replace('/', '-')
                df.to_excel(writer, sheet_name=sheet_name, index=False)
