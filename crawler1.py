import requests
from io import StringIO
import pandas as pd
import numpy as np
from datetime import date

datestr = date.today().strftime("%Y%m%d")

r = requests.post(
    'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')

# step3. 篩選出個股盤後資訊
str_list = []
for i in r.text.split('\n'):
    if len(i.split('",')) == 17 and i[0] != '=':
        i = i.strip(",\r\n")
        str_list.append(i)

# step4. 印出選股資訊
df = pd.read_csv(StringIO("\n".join(str_list)))
pd.set_option('display.max_rows', None)

# df.head(150)
df2 = df.loc[(pd.to_numeric(df['本益比'], errors='coerce') < 15) &
             (pd.to_numeric(df['本益比'], errors='coerce') > 0) & (pd.to_numeric(df['收盤價'], errors='coerce') < 50)].sort_values(by=['漲跌價差'])
df2
