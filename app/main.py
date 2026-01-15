
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 개발 환경에서는 현재 디렉토리의 main.py 실행
    if os.getenv("ENVIRONMENT") != "production":
        from app.main import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8080)
    else:
        # 프로덕션 환경에서는 Cloud Run 진입점
        from app.main import app
        
        # Google Cloud Functions 진입점 예시
        def ocr_function(request):
            return app(request)
