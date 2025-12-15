from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Passos Mágicos - Educational Risk Prediction", version="1.0.0")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "API is running. Go to /docs for Swagger UI."}
