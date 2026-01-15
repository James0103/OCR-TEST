from typing import Dict, Any, List
from app.services.google_vision import GoogleVisionService
from app.services.clova_ocr import ClovaOCRService

class OCRComparator:
    def __init__(self):
        self.google_service = GoogleVisionService()
        self.clova_service = ClovaOCRService()
    
    async def compare_ocr_results(self, image_content: bytes) -> Dict[str, Any]:
        # 두 OCR 서비스에서 결과 가져오기
        google_result = await self.google_service.extract_text(image_content)
        clova_result = await self.clova_service.extract_text(image_content)
        
        # 결과 비교 분석
        comparison = self._analyze_results(google_result, clova_result)
        
        return {
            "comparison": comparison,
            "google_vision": google_result,
            "naver_clova": clova_result,
            "timestamp": comparison.get("timestamp")
        }
    
    def _analyze_results(self, google_result: Dict, clova_result: Dict) -> Dict[str, Any]:
        import time
        
        google_text = google_result.get("full_text", "")
        clova_text = clova_result.get("full_text", "")
        
        # 텍스트 길이 비교
        google_length = len(google_text.strip())
        clova_length = len(clova_text.strip())
        
        # 처리 시간 비교
        google_time = google_result.get("process_time", 0)
        clova_time = clova_result.get("process_time", 0)
        
        # 유사도 계산 (간단한 문자열 비교)
        similarity = 0.0
        if google_text and clova_text:
            common_chars = set(google_text.lower()) & set(clova_text.lower())
            total_chars = set(google_text.lower()) | set(clova_text.lower())
            similarity = len(common_chars) / len(total_chars) if total_chars else 0.0
        
        return {
            "timestamp": int(time.time()),
            "text_length_comparison": {
                "google_vision": google_length,
                "naver_clova": clova_length
            },
            "processing_time_comparison": {
                "google_vision": google_time,
                "naver_clova": clova_time
            },
            "similarity_score": round(similarity * 100, 2),
            "both_successful": google_result.get("success", False) and clova_result.get("success", False),
            "recommendation": self._get_recommendation(google_result, clova_result, similarity, google_time, clova_time)
        }
    
    def _get_recommendation(self, google_result: Dict, clova_result: Dict, similarity: float, google_time: float = 0, clova_time: float = 0) -> str:
        google_success = google_result.get("success", False)
        clova_success = clova_result.get("success", False)
        
        if not google_success and not clova_success:
            return "Both OCR services failed. Please check the image quality."
        elif not google_success:
            return "Naver Clova OCR performed better for this image."
        elif not clova_success:
            return "Google Vision API performed better for this image."
        elif similarity > 80:
            return "Both services produced similar results. Either service would work well."
        elif len(google_result.get("full_text", "")) > len(clova_result.get("full_text", "")):
            return "Google Vision API extracted more text. Recommended for this image."
        else:
            return "Naver Clova OCR extracted more text. Recommended for this image."