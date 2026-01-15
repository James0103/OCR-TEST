from pydantic import BaseModel
from typing import Optional

class OCRRequest(BaseModel):
    file_base64: str
    save_to_sheet: bool = False
    sheet_name: str = "OCR Comparison"