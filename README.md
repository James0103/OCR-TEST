# OCR Test API

Google Vision API와 Naver Clova OCR을 비교 테스트하는 FastAPI 서비스

## 기능

- 이미지 업로드 및 OCR 처리
- Google Vision API 텍스트 추출
- Naver Clova OCR 텍스트 추출
- 두 서비스 결과 비교 분석
- 정확도 및 성능 비교

## API 엔드포인트

- `POST /api/v1/ocr/compare` - 두 OCR 서비스 비교
- `POST /api/v1/ocr/google-vision` - Google Vision API만 사용
- `POST /api/v1/ocr/naver-clova` - Naver Clova OCR만 사용
- `GET /api/v1/ocr/providers` - 제공 서비스 정보

## 로컬 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Cloud Run 배포

1. Google Cloud 프로젝트 ID 설정
2. 환경 변수 설정
3. 배포 스크립트 실행:

```bash
chmod +x deploy.sh
./deploy.sh
```

## 환경 변수

- `NCP_SECRET_KEY`: Naver Clova OCR 시크릿 키
- `NCP_OCR_URL`: Naver Clova OCR API URL
- `GOOGLE_CREDENTIALS_PATH`: Google Cloud 인증 파일 경로