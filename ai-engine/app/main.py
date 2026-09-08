from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AI Procurement Compliance Engine",
    version="0.1.0",
    description=(
        "AI-powered tender and bidder compliance analysis service."
    ),
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Procurement Compliance Engine",
        "status": "running",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }