from fastapi import FastAPI
from app.api.tenders import router as tender_router
from app.api.bidders import router as bidder_router
from app.api.bids import router as bid_router
from app.api.documents import router as document_router
from app.api.knowledge import router as knowledge_router

app = FastAPI(
    title="AI Procurement Compliance Platform",
    description="AI-powered bid compliance verification system for GeM procurement",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Procurement Compliance Platform",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }



app.include_router(tender_router)
app.include_router(bidder_router)
app.include_router(bid_router)
app.include_router(document_router)
app.include_router(knowledge_router)