from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ocr
import os

app = FastAPI(
    title="OCR Test API",
    description="Google Vision API & Naver Clova OCR 테스트 서비스",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router, prefix="/api/v1/ocr", tags=["OCR"])

@app.get("/")
async def root():
    return {"message": "OCR Test API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}