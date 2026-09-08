from fastapi import FastAPI
from app.api.routes import verification
from app.db.session import engine, Base
import app.db.models
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="AI Procurement Compliance - Verification Engine",
    version="0.1.0",
    description="Rule-based deterministic verification of bidder compliance for GeM procurement.",
)

app.include_router(verification.router)


@app.get("/health")
def health():
    return {"status": "ok"}
