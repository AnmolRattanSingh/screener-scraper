# read all files in folder output
import os
import glob


with open("top.txt", "r") as f:
    tickers = [ticker.strip() for ticker in f.readlines()]

output_dir = "output"
files = glob.glob(os.path.join(output_dir, "*.xlsx"))
excels = []
for file in files:
    excels.append(file.split(".")[0].split("/")[-1])

for excel in excels:
    print(excel)

# for ticker in tickers:
#     if ticker not in excels:
#         print(ticker)
