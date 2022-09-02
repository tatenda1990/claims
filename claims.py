import json
from pathlib import Path
import pandas as pd

def extract_all_travels(file_name):
    date = []
    location = []
    startTimeStamp = []
    endTimeStamp = []
    p = Path(__file__).with_name(file_name)
    with open(p) as f:
        data = json.load(f)
        a = data['timelineObjects']
        no_place_counter = 0
        no_name_counter = 0
        for i in range(1,len(a)+1,2): 
            try:
                if next(iter(a[i])) == 'placeVisit':
                    target = a[i]['placeVisit']
                elif next(iter(a[i])) == 'activitySegment':
                    target = a[i+1]['placeVisit'] #cater for the change in the 'placeVisit' index whih seems to be appearing in the json files for every month
                start_time = target['duration']['startTimestamp']
                end_time = target['duration']['endTimestamp']
                try:
                    location_data = target['location']['name']
                except:
                    print("Name Error at {}".format(start_time))
                    no_name_counter += 1
                #print (start_time.split("T")[0])
                date.append(start_time.split("T")[0])
                #print(location_data)
                location.append(location_data)
                #print(start_time)
                startTimeStamp.append(start_time)
                #print(end_time)
                endTimeStamp.append(end_time)
                #print()
            except:
                print("No placeVisit error")
                no_place_counter += 1
    print ("Number of noPlaceVisit key error is {}".format(no_place_counter))
    print ("Number of noNameError key error is {}".format(no_name_counter))
    return(date,location,startTimeStamp,endTimeStamp)

date = []
location = []
startTimeStamp = []
endTimeStamp = []

files = ['2022_APRIL.json','2022_MAY.json','2022_JUNE.json','2022_JULY.json','2022_AUGUST.json']
for file in files:
    info = extract_all_travels(file)
    date = date + (info[0])
    location = location + (info[1])
    startTimeStamp = startTimeStamp + (info[2])
    endTimeStamp = endTimeStamp + (info[3])

location_df = pd.DataFrame({ "Date": date,
                    "location": location,
                    "startTimeStamp": startTimeStamp,
                    "endTimeStamp": endTimeStamp
                    })
location_df['Date'] = pd.DatetimeIndex(location_df['Date'])

names = ['date', 'day', 'A', 'B','hrs','D']
claims_df = pd.read_csv('claims.csv', names = names)
claims_df.drop(["A","B","D"],axis = 1, inplace = True)
claims_df['date'] = pd.DatetimeIndex(claims_df['date'])
list_dates = []
target_location = "target_location"
for a in claims_df['date']:
    if (not((location_df[location_df["Date"] == a]['location'] == target_location).any())) == True:
        list_dates.append(a)
result = claims_df[claims_df['date'].isin(list_dates)]
result.reset_index(drop = True, inplace = True)
result.to_excel('result.xlsx')
print("Successful Run")