from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class OCRResult(BaseModel):
    provider: str
    full_text: str
    success: bool
    process_time: float
    error: Optional[str] = None

class ComparisonResult(BaseModel):
    timestamp: int
    text_length_comparison: Dict[str, int]
    processing_time_comparison: Dict[str, float]
    similarity_score: float
    both_successful: bool
    recommendation: str

class SheetInfo(BaseModel):
    saved: bool
    spreadsheet_url: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None

class OCRComparisonResponse(BaseModel):
    comparison: ComparisonResult
    google_vision: OCRResult
    naver_clova: OCRResult
    timestamp: int
    sheet_info: Optional[SheetInfo] = None