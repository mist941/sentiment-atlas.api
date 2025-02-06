from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get("/")
def read_root():
    return {"message": "Sentiment Atlas API"}
