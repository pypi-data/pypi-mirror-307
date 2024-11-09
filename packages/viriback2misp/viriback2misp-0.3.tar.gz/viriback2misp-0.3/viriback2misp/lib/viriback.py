import csv
from datetime import datetime as dt
import requests
from io import StringIO
import pandas as pd
from pathlib import Path

URLVIRIBACK = 'https://tracker.viriback.com/last30.php'
FILEPATH = 'viriback_bkp'

class C2():
    def __init__(self) -> None:
        try:
            response = requests.get(URLVIRIBACK, stream=True)
            response.raise_for_status()
            self.c2_content = response.text
            print(f"CSV file downloaded")
            pass
        except Exception as err:
            print(f"Could not no access the c2 content: {err}")
    
    def get_C2(self) -> dict:
        self.update_bkp_file()
        file = self.csv_to_dict()
        return self.split_by_month(file)
    
    def update_bkp_file(self):
        online_df = pd.read_csv(StringIO(self.c2_content))
        bkp_file = Path(FILEPATH)
        if not bkp_file.exists():
            online_df.to_csv(FILEPATH, index=False, date_format='%d-%m-%Y')
            return 
        local_df = pd.read_csv(FILEPATH)

        new_entries_df = self.find_new_entries(online_df, local_df)
        new_entries_df.to_csv(FILEPATH, index=False, date_format='%d-%m-%Y')
        

    def find_new_entries(self, online_df, local_df):
        """
        Get only the data in online equal or newer than the last update of local_df
        Input: Two dataframes
        Output: Dataframe
        """
        online_df['FirstSeen'] = pd.to_datetime(online_df['FirstSeen'], format='%d-%m-%Y')
        local_df['FirstSeen'] = pd.to_datetime(local_df['FirstSeen'], format='%d-%m-%Y')

        latest_date_in_old = local_df['FirstSeen'].max()
        new_df = online_df[online_df['FirstSeen'] >= latest_date_in_old]
        return new_df

    def csv_to_dict(self) -> dict:
        c2 = []
        with open(FILEPATH, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
        
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    line = {"family": row[0], "url": row[1], "ip": row[2], "firstseen": row[3]}
                    c2.append(line)
                    line_count += 1
            print(f'Processed {line_count - 1} lines.')
            return c2

    def split_by_month(self, data:list) -> dict:
        c2_by_month = {}
        for item in data:
            date_str = item.get('firstseen')
            date_dt = dt.strptime(date_str, "%d-%m-%Y")
            month_year = date_dt.strftime("%Y-%m")
            c2_by_month.setdefault(month_year, [])
            c2_by_month[month_year].append(item)
        return c2_by_month
    
    def family_trends(data:list, num:int=10):
        family = {}
        for item in data:
            family.setdefault(item["family"], 0)
            family[item["family"]] += 1

        sorted_family = dict(sorted(family.items(), key=lambda item: item[1], reverse=True))
        x_items = {k: sorted_family[k] for k in list(sorted_family.keys())[:num]}
        return x_items
    

    def split_by_family(self, data:list) -> dict:
        c2_by_family = {}
        for item in data:
            family = item.get("family")
            c2_by_family.setdefault(family, [])
            c2_by_family[family].append(item)
        return c2_by_family

    def dif_content():
        pass

