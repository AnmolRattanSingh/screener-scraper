import os
import pandas as pd

def extract_peers_sheets(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Iterate through all Excel files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            source_file_path = os.path.join(source_folder, filename)
            
            # Load the Excel file
            xls = pd.ExcelFile(source_file_path)
            
            # Check if the "Peers" sheet exists in the Excel file
            if "Peers" in xls.sheet_names:
                df_peers = pd.read_excel(source_file_path, sheet_name="Peers")
                
                # Save the "Peers" sheet to a new Excel file in the destination folder
                destination_file_path = os.path.join(destination_folder, filename)
                with pd.ExcelWriter(destination_file_path, engine='xlsxwriter') as writer:
                    df_peers.to_excel(writer, sheet_name="Peers", index=False)
                
                print(f"Extracted 'Peers' sheet from {filename} and saved to {destination_file_path}")
            else:
                print(f"'Peers' sheet not found in {filename}")

# Specify the source and destination folders
source_folder = "./output"
destination_folder = "./peers"

# Call the function to extract "Peers" sheets
extract_peers_sheets(source_folder, destination_folder)
