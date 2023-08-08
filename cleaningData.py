import pandas as pd
import os
import re

# Change the folder directory
folder_path = '/Users/abdulsalamhijazikelani/Desktop/parsing-data/'


excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

for excel_file in excel_files:
    file_path = os.path.join(folder_path, excel_file)
    df = pd.read_excel(file_path)

    def extract_details(details_str, keyword):
        if isinstance(details_str, str) and keyword in details_str:
            start_idx = details_str.index(keyword) + len(keyword)
            end_idx = details_str.find("View all details", start_idx)
            return details_str[start_idx:end_idx].strip()
        return None

    df['PRICE RANGE'] = df['Details'].apply(lambda x: extract_details(x, "PRICE RANGE"))
    df['CUISINES'] = df['Details'].apply(lambda x: extract_details(x, "CUISINES"))
    df['MEALS'] = df['Details'].apply(lambda x: extract_details(x, "Meals"))

    df['PRICE RANGE'] = df['PRICE RANGE'].str.split("CUISINES", expand=True)[0].str.strip()
    df['CUISINES'] = df['CUISINES'].str.split("Meals", expand=True)[0].str.strip()

    columns_to_drop = ['web-scraper-order', 'web-scraper-start-url', 'links', 'links-href']
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=columns_to_drop_existing, inplace=True)

    df['Email'] = df['Email'].str.replace('mailto:', '').str.replace('?subject=?', '')

    def clean_food_types(data):
        if isinstance(data, str):
            data = re.sub(r'"Food Type":', '', data)
            types = re.findall(r'[^,]+', data)
            types = [t.strip() for t in types if t.strip()]
            data = ', '.join(types)
        return data

    df['Food Type'] = df['Food Type'].apply(clean_food_types)
    df['Food Type'] = df['Food Type'].str.replace('[', '').str.replace(']', '').str.replace('{', '').str.replace('}', '').str.replace('"', '')

    df['Time'] = df['Time'].str.replace('Open now:', '').str.replace('Closed now: See all hours', '').str.strip()
    df['Time'] = df['Time'].str.replace('Closed now:  See all hours', '').str.strip()
    df['Time'] = df['Time'].apply(lambda x: '' if pd.isna(x) or 'See all hours' in x else x)

    if 'Price Range' in df.columns:
        df.drop(columns=['Price Range'], inplace=True)

    df.drop(columns=['Details'], inplace=True)

    df.to_excel(file_path, index=False)
