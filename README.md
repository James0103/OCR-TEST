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

## 검증 계획

### 분석 방식
1. **기본 지표**: CER, WER, 필드 정확도
2. **비즈니스 가치**: 상품명/가격 추출 정확도
3. **처리 효율**: 처리 시간 비교
4. **품질 영향**: 이미지 품질별 성능 비교

### 검증 체계
1. **단일 테스트**: 영수증 1개씩 수동 진행
2. **배치 테스트**: 다수 영수증 자동화
3. **결과 집계**: Google Sheets에서 통계 분석
4. **최종 보고**: 성능 비교 및 추천

## 🎯 핵심 지표
- **CER** (Character Error Rate): 문자 수준 오류율
- **WER** (Word Error Rate): 단어 수준 오류율
- **Field Accuracy**: 상품명/가격 등 구조화된 정보 정확도
- **Processing Speed**: 평균 처리 시간

## 🚀 실행 단계
1. **기반 구축**: 데이터셋 및 스프레드시트 준비
2. **단일 검증**: 샘플 테스트로 기능 검증
3. **배치 분석**: 실제 데이터로 성능 측정
4. **최종 보고**: 객관적 성능 비교 및 권장사항