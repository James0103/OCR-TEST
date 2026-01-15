import os
from dotenv import load_dotenv, find_dotenv

# .env 파일 명시적 로드
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    load_dotenv()  # fallback

class Settings:
    # Google Cloud
    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    
    # Naver Clova OCR
    NCP_SECRET_KEY = os.getenv("NCP_SECRET_KEY")
    NCP_OCR_URL = os.getenv("NCP_OCR_URL")
    
    # Google Sheets
    SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "OCR Results Comparison")
    SPREADSHEET_URL = os.getenv("SPREADSHEET_URL", "")
    
    # App settings
    UPLOAD_DIR = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
settings = Settings()