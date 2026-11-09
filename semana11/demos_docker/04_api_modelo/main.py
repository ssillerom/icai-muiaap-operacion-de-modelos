import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Iris API")
model = joblib.load("models/model.joblib")
CLASES = ["setosa", "versicolor", "virginica"]

class Flor(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(f: Flor):
    X = [[f.sepal_length, f.sepal_width,
          f.petal_length, f.petal_width]]
    return {"clase": CLASES[int(model.predict(X)[0])]}
