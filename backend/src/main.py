from fastapi import FastAPI

app = FastAPI(title="Expenses API")


@app.get("/health")
async def health():
    return {"status": "ok"}
