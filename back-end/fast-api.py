from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend import predict, race, create_df
from pydantic import BaseModel
import joblib
from xgboost import XGBClassifier
import uvicorn
import pandas as pd
import numpy as np
from pyproj import Proj, transform

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="front-end")
model = joblib.load(r".\XGBoost.joblib")

class info(BaseModel):
    gender:str
    race:str
    age:int
    day:int
    month:int
    year:int
    hour:int
    place:str
    lat:float
    lon:float
    
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

@app.post("/prediction")
async def make_prediction(user_info:info):
    inproj = Proj(init='epsg:3857')
    outproj = Proj(init='epsg:4326')
    x2,y2 = transform(inproj, outproj, user_info.lon, user_info.lat)
    print(user_info.lon, user_info.lat)
    print(x2, y2)
    df = create_df(user_info.hour,user_info.month,user_info.day,user_info.year,y2,x2,user_info.place,user_info.age,user_info.race,user_info.gender)
    pred = predict(df)
    return {"result": pred}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='localhost')