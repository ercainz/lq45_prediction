import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

from pipeline_predicting import pipeline
from global_func import api_homepage

class InputData(BaseModel):
    date: str = Field(default='yyyymmdd', min_length=8, max_length=8)
    jci: float = Field(default=7000, gt=1000, le=20000)
    idx30: float = Field(default=500, gt=100, le=5000)
    eido: float = Field(default=24.00, gt=1, le=200)
    spy: float = Field(default=400, gt=1, le=5000)
    dom_b: float = Field(default=1.00, gt=0, le=100)
    dom_s: float = Field(default=1.00, gt=0, le=100)
    for_b: float = Field(default=1.00, gt=0, le=100)
    for_s: float = Field(default=1.00, gt=0, le=100)
#==========================================================================================================================#
#==========================================================================================================================#
app = FastAPI()
#==========================================================================================================================#
#==========================================================================================================================#
@app.get("/")
def home():
    sample_input = {
                    "date": "20220328",
                    "jci": 7049.6030,
                    "idx30": 549.373,
                    "eido": 24.92,
                    "spy": 455.91,
                    "dom_b": 9.9995,
                    "dom_s": 10.8573,
                    "for_b": 4.2166,
                    "for_s": 3.3587
                    }
    
    return {"PROJECT DETAIL": api_homepage(),
            "SAMPLE INPUT": sample_input}
#==========================================================================================================================#
#==========================================================================================================================#
@app.post("/pred/")
def predict(data: InputData):
    data = pd.DataFrame(data).set_index(0).T.reset_index(drop=True)

    input_list = [data.date[0],
                  data.jci[0],
                  data.idx30[0],
                  data.eido[0],
                  data.spy[0],
                  data.dom_b[0],
                  data.dom_s[0],
                  data.for_b[0],
                  data.for_s[0]]

    api_return = pipeline(data_from_api=input_list) 

    return {'input_date': api_return[0],
            'pred_value':api_return[1],
            'pred_desc':api_return[2]}
#==========================================================================================================================#
#==========================================================================================================================#
if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8080)
