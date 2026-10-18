from fastapi import FastAPI
from app.routers import batteries, telemetry

app = FastAPI(title="GridOS")

app.include_router(batteries.router)
app.include_router(telemetry.router)


@app.get("/health")
def health():
    return {"status": "ok"}