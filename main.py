from fastapi import FastAPI, Request, Response, HTTPException, Header
from fastapi.responses import StreamingResponse
import pandas as pd

app = FastAPI()

df = pd.read_csv('data.csv')


@app.get("/")  # main endpoint
def getDataframe():
    return df.to_dict(orient="records")


@app.get("/protected") #berpassword
def protect(api_key: str = Header(None)):

    if api_key is None or api_key != "secret123":
        # handle error
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "message": "This endpoint is protected by API Token Key.",
        "data": {
            "1": {"username": "fahmi", "password": "1234"},
            "2": {"username": "raka", "password": "abcd123"},
            "3": {"username": "rachman", "password": "h8teacher"}
        }
    }


@app.get("/json") # memanggil list dalam bentuk json
def get_json_data():
    df = pd.DataFrame(
        [["Canada", 10], ["USA", 20]], 
        columns=["team", "points"]
    )
    return df.to_dict(orient="records")


@app.get("/csv") #convert list ke csv
def get_csv_data():
    df = pd.DataFrame(
        [["Canada", 10], ["USA", 20]], 
        columns=["team", "points"]
    )
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
)