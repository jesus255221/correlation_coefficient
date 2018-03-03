import json
from numpy import *
import datetime

def mean_value(data,cursor):
    if cursor == 0:
        return data[cursor + 1]
    elif cursor == (len(data) - 1):
        return data[cursor - 1]
    elif cursor >= 1: 
        i,j = 1,1
        while data[cursor - i] == 0:
            i = i + 1
        while data[cursor + j] == 0:
            j = j + 1  
        return (data[cursor - i] + data[cursor + j]) / 2


with open("Jilong_2017_winter_pm25.json","r") as JiLong:# From 9/1 0.00
    with open("NingBo","r") as NingBo:# From 9/1 1:00
        # 6hrs 
        JiLong_Data = json.loads(JiLong.read())#9/17 3~8 Missing
        NingBo_Data = json.loads(NingBo.read())
        JiLong_PM25 = []
        NingBo_PM25 = [0]*720
        for data in JiLong_Data:
            if data['date']['month'] == 9 and data['date']['day'] <= 30:# If the data is in range
#                print(data)
                day = [0]*24# Set an array to store pm25 data of a day
                for pm25 in data['hr_data']:
                    day[pm25['hr_t']] = pm25['hr_v']# Set the corresponding value to the corresponding time
#                    print(pm25['hr_v'])
#                    print(data['date']['month'],'/',data['date']['day'],pm25['hr_t'])
                for item in range(0,len(day)): #Detect Missing
                    if day[item] == 0 or day[item] == -1:
#                        print(data['date']['month'],'/',data['date']['day'],item,'Missing!')
                        print(item)
                        day[item] = mean_value(day,item)# Fake data
                JiLong_PM25.extend(day)
        print(JiLong_PM25)
        print(len(JiLong_PM25[7:]))
        date_cursor = datetime.datetime(2017,9,1,0,0,0)
        cursor = 0
        for data in NingBo_Data:
            if data[0] != date_cursor.strftime('%Y-%m-%d %H:%M:%S'):# Detect whether the date is right
                if(NingBo_PM25[cursor] == 0):# Detect Missing
                    print(date_cursor.strftime('%Y-%m-%d %H:%M:%S'),'Missing!')
                cursor = cursor + 1# Move the cursor
                date_cursor += datetime.timedelta(hours = 1)
            if data[2] == "\u533a\u73af\u4fdd\u5927\u697c":# If the data exist
                NingBo_PM25[cursor] = int(data[6])
#                print(data)
#            print(date_cursor.strftime('%Y-%m-%d %H:%M:%S'))
#            if data[2] == "\u533a\u73af\u4fdd\u5927\u697c" and len(NingBo_PM25) <= 720:
        NingBo_PM25[0] = 14
        for index in range(0,len(NingBo_PM25)):
            if(NingBo_PM25[index] == 0):
                NingBo_PM25[index] = NingBo_PM25[index - 1]
        print(NingBo_PM25)
        print(len(NingBo_PM25[:713]))
        for s in range(0,24):
            JiLong_PM25_np = array(JiLong_PM25[s:])
            NingBo_PM25_np = array(NingBo_PM25[:(720-s)])
            print(corrcoef([JiLong_PM25_np,NingBo_PM25_np]))


