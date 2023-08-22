import pandas as pd
import os

# Change the folder directory
folder_path = '/Users/abdulsalamhijazikelani/Desktop/test'

columns_to_drop = ['web-scraper-order', 'web-scraper-start-url', 'links-href']

excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

for excel_file in excel_files:
    file_path = os.path.join(folder_path, excel_file)
    df = pd.read_excel(file_path)
    df.drop(columns=columns_to_drop, inplace=True)
    df['Review'] = df['Review'].str.rstrip('More')
    df['Score'] = df['Score'].str.replace('ui_bubble_rating bubble_', '')
    df.rename(columns={'links': 'Restaurant Name'}, inplace=True)
    df.to_excel(file_path, index=False)
