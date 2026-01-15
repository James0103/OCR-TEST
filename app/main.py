# import os
# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# if __name__ == "__main__":
#     # 개발 환경에서는 현재 디렉토리의 main.py 실행
#     if os.getenv("ENVIRONMENT") != "production":
#         from app.main import app
#         import uvicorn
#         uvicorn.run(app, host="0.0.0.0", port=8080)
#     else:
#         # 프로덕션 환경에서는 Cloud Run 진입점
#         from app.main import app
        
#         # Google Cloud Functions 진입점 예시
#         def ocr_function(request):
#             return app(request)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 추가
from .api.ocr import router as ocr_router
import os

app = FastAPI()
# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 테스트를 위해 전체 허용, 이후 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr_router, prefix="/api", tags=["OCR"])

@app.get("/")
def health_check():
    return {"status": "OCR API Running"}

@app.post("/ocr")
async def ocr_process():
    return {"text": "테스트"}

# 로컬 테스트용 (Railway에서는 실행 안 됨)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)