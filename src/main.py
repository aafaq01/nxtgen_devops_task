from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Add Prometheus metrics
@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}