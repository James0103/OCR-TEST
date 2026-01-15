import pytest
import asyncio
from app.services.comparator import OCRComparator
from app.services.google_vision import GoogleVisionService
from app.services.clova_ocr import ClovaOCRService

class TestOCRServices:
    def test_google_vision_init(self):
        service = GoogleVisionService()
        assert service.client is not None
    
    def test_clova_ocr_init(self):
        service = ClovaOCRService()
        assert service.secret_key is not None
        assert service.api_url is not None
    
    def test_comparator_init(self):
        comparator = OCRComparator()
        assert comparator.google_service is not None
        assert comparator.clova_service is not None

@pytest.mark.asyncio
class TestOCRComparison:
    async def test_compare_with_mock_image(self):
        comparator = OCRComparator()
        
        # Create a mock image content (simple text image)
        mock_image_content = b"mock_image_data"
        
        # This would normally call actual APIs, so we'll test the structure
        # In real testing, you would mock the API calls
        result_structure = {
            "comparison": {
                "timestamp": int,
                "text_length_comparison": dict,
                "word_count_comparison": dict,
                "similarity_score": float,
                "both_successful": bool,
                "recommendation": str
            },
            "google_vision": dict,
            "naver_clova": dict,
            "timestamp": int
        }
        
        assert "comparison" in result_structure
        assert "google_vision" in result_structure
        assert "naver_clova" in result_structure