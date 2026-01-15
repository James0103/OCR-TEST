from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import aiofiles
import os
from typing import Dict, Any

from app.services.comparator import OCRComparator
from app.services.google_sheets import GoogleSheetsService
from app.models.schemas import OCRComparisonResponse
from app.core.config import settings

router = APIRouter()
comparator = OCRComparator()
sheets_service = GoogleSheetsService()

@router.post("/compare", response_model=OCRComparisonResponse)
async def compare_ocr(file: UploadFile = File(...), save_to_sheet: bool = Form(False), sheet_name: str = Form("OCR Comparison")):
    print(f"🔍 [API] 파라미터 수신: save_to_sheet={save_to_sheet}, sheet_name={sheet_name}")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    try:
        image_content = await file.read()
        result = await comparator.compare_ocr_results(image_content)
        
        # Google Sheets에 저장 옵션
        if save_to_sheet:
            try:
                print(f"🔍 시트 저장 시작: sheet_name={sheet_name}")
                print(f"📊 OCR 결과 받음: google_success={result['google_vision'].get('success')}, naver_success={result['naver_clova'].get('success')}")
                
                # 스프레드시트 연결
                spreadsheet_url = settings.SPREADSHEET_URL
                if spreadsheet_url:
                    print(f"🔗 기존 스프레드시트 연결: {spreadsheet_url}")
                    sheets_service.get_or_create_spreadsheet(spreadsheet_url=spreadsheet_url)
                else:
                    print(f"🆕 새 스프레드시트 생성: {settings.SPREADSHEET_NAME}")
                    sheets_service.get_or_create_spreadsheet()
                
                print(f"✅ 스프레드시트 준비 완료")
                
                # 데이터 저장
                save_result = sheets_service.save_ocr_results(
                    image_name=file.filename,
                    image_size=file.size,
                    google_result=result["google_vision"],
                    naver_result=result["naver_clova"],
                    comparison_result=result["comparison"],
                    sheet_name=sheet_name
                )
                
                print(f"💾 시트 저장 완료: {save_result}")
                
                # 시트 정보 추가
                result["sheet_info"] = {
                    "saved": True,
                    "spreadsheet_url": sheets_service.get_spreadsheet_url(),
                    "sheet_name": sheet_name,
                    "message": save_result
                }
            except Exception as sheet_error:
                print(f"❌ 시트 저장 실패: {sheet_error}")
                import traceback
                traceback.print_exc()
                result["sheet_info"] = {
                    "saved": False,
                    "error": str(sheet_error),
                    "sheet_name": sheet_name
                }
        else:
            print("📝 시트 저장 요청 안함")
            result["sheet_info"] = {
                "saved": False,
                "message": "Not requested to save to sheet",
                "sheet_name": sheet_name
            }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/google-vision")
async def google_vision_ocr(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_content = await file.read()
        result = await comparator.google_service.extract_text(image_content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/naver-clova")
async def naver_clova_ocr(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_content = await file.read()
        result = await comparator.clova_service.extract_text(image_content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_providers():
    return {
        "providers": [
            {
                "name": "google_vision",
                "description": "Google Cloud Vision API - 강력한 다국어 OCR 지원"
            },
            {
                "name": "naver_clova",
                "description": "Naver Clova OCR - 한글 인식에 최적화"
            }
        ]
    }

@router.post("/test-sheet")
async def test_sheet_save(sheet_name: str = "test", test_data: str = "test message"):
    """시트 저장 테스트 엔드포인트"""
    try:
        # 샘플 OCR 결과 데이터 생성
        sample_google = {
            "success": True,
            "full_text": f"Google OCR test: {test_data}",
            "process_time": 123.45
        }
        
        sample_naver = {
            "success": True,
            "full_text": f"Naver OCR test: {test_data}",
            "process_time": 98.76
        }
        
        sample_comparison = {
            "similarity_score": 85.5,
            "both_successful": True,
            "recommendation": "Test completed successfully"
        }
        
        # Google Sheets에 저장
        spreadsheet_url = settings.SPREADSHEET_URL
        sheets_service.get_or_create_spreadsheet(spreadsheet_url=spreadsheet_url if spreadsheet_url else None)
        
        save_result = sheets_service.save_ocr_results(
            image_name=f"test_{test_data}.jpg",
            image_size=2048,
            google_result=sample_google,
            naver_result=sample_naver,
            comparison_result=sample_comparison,
            sheet_name=sheet_name
        )
        
        return {
            "success": True,
            "message": f"Test data saved to sheet '{sheet_name}'",
            "sheet_name": sheet_name,
            "test_data": test_data,
            "spreadsheet_url": sheets_service.get_spreadsheet_url(),
            "save_result": save_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to save test data: {str(e)}",
            "error": str(e)
        }
