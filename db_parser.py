import pandas as pd
from firebase import firebase
import math

firebase = firebase.FirebaseApplication('https://gravitel-d0c7e.firebaseio.com', None)
df = pd.read_csv('data/timesData.csv')
cats = df.columns.values.tolist()
for index in range(1803+720, 2603):
    print(df.iloc[index])
    uni_name = str(index - 1802)
    print(uni_name)
    for i in range(0, len(cats)):
        myData = df.iloc[index][cats[i]]
        if hasattr(myData, 'item'):
            myData = myData.item()
        if not isinstance(myData, str):
            if math.isnan(myData):
                continue
        firebase.put('/unis/' + uni_name, name=cats[i], data=myData, params={'print': 'pretty'})
