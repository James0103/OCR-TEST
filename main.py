#!/usr/bin/env python3
"""
OCR Validation - 메인 진입점 (Root Level)
"""

import os
import sys

# Add app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import OCR API
from app.api.ocr import router as ocr_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app at root level
app = FastAPI(
    title="OCR Validation API",
    description="Google Vision vs Naver Clova OCR 성능 검증 서비스",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include OCR routes from app.api.ocr
app.include_router(ocr_router, prefix="/api/v1/ocr", tags=["OCR"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "OCR Validation API is running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    # Get server configuration
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("🚀 OCR Validation API Starting...")
    print(f"📋 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🌐 Server: http://{host}:{port}")
    
    # Run server
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )