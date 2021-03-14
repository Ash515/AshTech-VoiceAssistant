import pandas as pd
from pandas import read_csv, DataFrame
import datetime

df = read_csv("bday.csv",sep=',')
df = DataFrame(df,columns=['name','mon','date'])

day = datetime.datetime.now().day
month = datetime.datetime.now().month

Blist=[]
for i in range(4):
    try: 
        if month == df['mon'][i]:
            if day == df['date'][i]:
                Blist.append(df['name'][i])
    except:
        break
print("Today's the Birthday of: ")
for name in Blist:
    print(name)