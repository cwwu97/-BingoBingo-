from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

from tqdm import tqdm, trange

def crawler(start_date, end_date):

    result = pd.DataFrame()
    current_date = start_date
    progress = tqdm(total = (end_date - start_date).days)

    while current_date < end_date:

        url = 'https://lotto.auzonet.com/bingobingo/list_{}.html'.format(str(current_date.year)+str(current_date.month).zfill(2)+str(current_date.day).zfill(2))
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        date_ = soup.find_all('b')[4].getText().split('\xa0\xa0')[-1][1:-1]
        bingo_rows = soup.find_all('tr', class_='bingo_row')

        for i in range(len(bingo_rows)):
            single_row = bingo_rows[i].getText(',').split(',')
            single_row[1] = date_ +' '+single_row[1]
            if len(single_row) == 24:
                result = result.append(pd.Series(single_row, 
                                        index = ['ID', 'Datetime', 'Num01', 'Num02', 'Num03', 'Num04', 'Num05', 'Num06', 'Num07', 'Num08', 'Num09', 'Num10',
                                                'Num11', 'Num12', 'Num13','Num14','Num15','Num16','Num17','Num18','Num19','Num20', 'Consecutive_num', 'Odd/Even']),
                                        ignore_index=True)
            elif len(single_row) == 25:
                del single_row[-2]
                result = result.append(pd.Series(single_row, 
                                        index = ['ID', 'Datetime', 'Num01', 'Num02', 'Num03', 'Num04', 'Num05', 'Num06', 'Num07', 'Num08', 'Num09', 'Num10',
                                                'Num11', 'Num12', 'Num13','Num14','Num15','Num16','Num17','Num18','Num19','Num20', 'Consecutive_num', 'Odd/Even']),

                                        ignore_index=True)

        progress.update(1)    
        current_date += timedelta(days=1)
        
    result = result[['ID', 'Datetime', 'Num01', 'Num02', 'Num03', 'Num04', 'Num05', 'Num06', 'Num07', 'Num08', 'Num09', 'Num10',
                                                'Num11', 'Num12', 'Num13','Num14','Num15','Num16','Num17','Num18','Num19','Num20', 'Consecutive_num', 'Odd/Even']]

    return result.sort_values(by = 'ID').reset_index(drop = True, inplace = True)



if __name__ == '__main__':
    

    start_date = datetime.strptime(input('Enter a start date (format = YYYY-MM-DD):'), '%Y-%m-%d').date()
    end_date = datetime.strptime(input('Enter a end date (format = YYYY-MM-DD):'), '%Y-%m-%d').date()
    result = crawler(start_date, end_date)

    result.to_csv('./bingobingo.csv', index = False)