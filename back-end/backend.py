from numpy.lib.shape_base import expand_dims
import pandas as pd
import numpy as np
import joblib
import numpy as np
import pandas as pd
import re
import os



# Import models

from xgboost import XGBClassifier




model = joblib.load(r".\XGBoost.joblib")
def race(r):
    if(r == "WHITE"):
        return 7
    if(r == "WHITE HISPANIC"):
        return 6
    if(r == "BLACK"):
        return 5
    if(r == "ASIAN / PACIFIC ISLANDER"):
        return 4
    if(r == "BLACK HISPANIC"):
        return 3
    if(r == "AMERICAN INDIAN/ALASKAN NATIVE"):
        return 2
    if(r == "OTHER"):
        return 1
    else :
        return 0
def sex(s):
    if(s == "F"):
        return 4
    if(s == "M"):
        return 3
    if(s == "D"):
        return 2
    if(s == "E"):
        return 1
    else : 
        return 0
def week_day(month, day, year):
    date=str(month)+"/"+str(day)+"/"+str(year)
    d = pd.Timestamp(date)
    day=d.day_name()
    return(day)
def create_df(hour,month,day,year,latitude,longitude,place,vic_age,vic_race,vic_sex):
    hour = int(hour) if int(hour) < 24 else 0
    api_data = None
    """try:
      api_data = requests.get(f'{api_endpoint}{longitude},{latitude}&distance=1000&token={api_token}').json()['address']
      pct, b = int(api_data["policePrecinct"]),api_data["Borough"]
      boro = boro.upper()
    except Exception as e:
       print(e)"""
    year = int(year)
    month = int(month)
    day = int(day)
    #dat = datetime(year=year, month=month, day=day)
    #weekday = dat.weekday() #Monday is 0 and Sunday is 6

    in_park = 1 if place == "In park" else 0
    in_public = 1 if place == "In public housing" else 0
    in_station = 1 if place == "In station" else 0
    #b = boro(b)
    vic_race = race(vic_race)
    vic_sex= sex(vic_sex)
    weekday= (week_day(month, day, year)).upper()
    

    columns = np.array([ 'IN_PARK', 'IN_PUBLIC_HOUSING', 'Latitude', 'Longitude', 'IN_STATION', 
                        'VIC_RACE', 'VIC_SEX', 'year', 'month', 'day', 'hour', 'VIC_AGE_GROUP_18-24', 'VIC_AGE_GROUP_25-44',
                        'VIC_AGE_GROUP_45-64', 'VIC_AGE_GROUP_65+', 'VIC_AGE_GROUP_-18', 'VIC_AGE_GROUP_UNKNOWN',
                        'weekday_Friday', 'weekday_Monday', 'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday',
                        'weekday_Tuesday', 'weekday_Wednesday'])
    
    data = [[in_park,
             in_public,
             latitude,
             longitude,
             in_station,
             vic_race,
             vic_sex,
             year, month, day,hour,
             1 if vic_age in range(18,25) else 0, 
             1 if vic_age in range(25,45) else 0, 
             1 if vic_age in range(45,65) else 0, 
             1 if vic_age>=65 else 0,
             1 if vic_age < 18 else 0,
             0,
             1 if weekday == "FRIDAY" else 0,
             1 if weekday == "MONDAY" else 0,
             1 if weekday == "SATURDAY" else 0,
             1 if weekday == "SUNDAY" else 0,
             1 if weekday == "THURSDAY" else 0,
             1 if weekday == "TUESDAY" else 0,
             1 if weekday == "WEDNESDAY" else 0,
             
       ]]

    df = pd.DataFrame(data,columns=columns)
    return df.values
data= create_df(7,10,12,2016,40.636991,-74.134093,'',50,"WHITE HISPANIC","F")
crime_types = {0:'Violation',1:"Misdemeanor",2:"Felony"}

def predict(data):
   pred = model.predict(data)[0]
   if (pred == 0):
      return crime_types[pred]
   elif pred==1:
      return crime_types[pred]
   else:
      return crime_types[pred]
print(predict(data))
