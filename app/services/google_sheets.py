import os
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any
from app.core.config import settings
import json
from datetime import datetime

class GoogleSheetsService:
    def __init__(self):
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # 환경 변수에서 자격증명 정보 읽기
        if os.getenv("GOOGLE_CREDENTIALS_JSON"):
            credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
            self.credentials = Credentials.from_service_account_info(
                credentials_info, 
                scopes=self.scope
            )
        elif settings.GOOGLE_CREDENTIALS_PATH and os.path.exists(settings.GOOGLE_CREDENTIALS_PATH):
            self.credentials = Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                scopes=self.scope
            )
        else:
            raise ValueError("Google credentials not found. Please set GOOGLE_CREDENTIALS_JSON or GOOGLE_CREDENTIALS_PATH")
        
        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet = None
    
    def get_or_create_spreadsheet(self, name: str = None, spreadsheet_url: str = None):
        spreadsheet_name = name or settings.SPREADSHEET_NAME
        
        try:
            if spreadsheet_url:
                # URL에서 스프레드시트 ID 추출하여 직접 접근
                import re
                match = re.search(r'/d/([a-zA-Z0-9-_]+)', spreadsheet_url)
                if match:
                    spreadsheet_id = match.group(1)
                    self.spreadsheet = self.gc.open_by_key(spreadsheet_id)
                    print(f"스프레드시트 '{spreadsheet_name}'에 성공적으로 연결되었습니다.")
                    return self.spreadsheet
                else:
                    raise ValueError("Invalid spreadsheet URL format")
            else:
                # 기존 스프레드시트 찾기
                self.spreadsheet = self.gc.open(spreadsheet_name)
                print(f"기존 스프레드시트 '{spreadsheet_name}'을 찾았습니다.")
        except gspread.exceptions.SpreadsheetNotFound:
            raise ValueError(
                f"스프레드시트 '{spreadsheet_name}'을 찾을 수 없습니다.\n"
                "1. 기존 스프레드시트를 만드세요: https://sheets.google.com\n"
                "2. 서비스 계정 이메일({})을 공유하세요: \n"
                "   - 파일 > 공유 > 편집자로 추가\n"
                "3. spreadsheet_url 또는 URL을 설정하세요"
                .format(self.credentials.service_account_email if self.credentials else "unknown")
            )
            
        return self.spreadsheet
    
    def setup_comparison_sheet(self, sheet_name: str = "OCR Comparison"):
        """OCR 비교 결과를 위한 워크시트 설정"""
        if not self.spreadsheet:
            self.get_or_create_spreadsheet()
        
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            # 기존 워크시트의 경우 헤더 확인
            all_values = worksheet.get_all_values()
            if not all_values:  # 비어있으면 헤더 추가
                self._add_headers(worksheet)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(sheet_name, 1000, 20)
            self._add_headers(worksheet)
        
        return worksheet
    
    def _add_headers(self, worksheet):
        """워크시트에 헤더 추가"""
        headers = [
            "Timestamp", "Image_Name", "Image_Size",
            "Google_Success", "Google_Text_Length", "Google_Full_Text", "Google_Processing_Time",
            "Naver_Success", "Naver_Text_Length", "Naver_Full_Text", "Naver_Processing_Time",
            "Similarity_Score", "Both_Successful", "Recommendation"
        ]
        worksheet.append_row(headers)
        worksheet.format('A1:N1', {
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
            'textFormat': {'bold': True}
        })
    
    def save_ocr_results(self, image_name: str, image_size: int, 
                       google_result: Dict, naver_result: Dict, 
                       comparison_result: Dict, sheet_name: str = "OCR Comparison") -> str:
        """OCR 결과 저장"""
        print(f"🔧 [SHEETS SERVICE] save_ocr_results 시작")
        print(f"   - sheet_name: {sheet_name}")
        print(f"   - image_name: {image_name}")
        print(f"   - google_success: {google_result.get('success')}")
        print(f"   - naver_success: {naver_result.get('success')}")
        
        try:
            worksheet = self.setup_comparison_sheet(sheet_name)
            print(f"✅ [SHEETS SERVICE] 워크시트 준비 완료")
            
            # 데이터 준비
            all_values = worksheet.get_all_values()
            current_row_count = len(all_values)
            print(f"📊 [SHEETS SERVICE] 현재 행 수: {current_row_count}")
            
            # 데이터 준비
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
                image_name,  # Image_Name
                f"{image_size/1024:.2f} KB",  # Image_Size
                
                # Google Results
                google_result.get("success", False),  # Google_Success
                len(google_result.get("full_text", "")),  # Google_Text_Length
                google_result.get("full_text", ""),  # Google_Full_Text
                f"{google_result.get('process_time', 0)} ms",  # Google_Processing_Time
                
                # Naver Results
                naver_result.get("success", False),  # Naver_Success
                len(naver_result.get("full_text", "")),  # Naver_Text_Length
                naver_result.get("full_text", ""),  # Naver_Full_Text
                f"{naver_result.get('process_time', 0)} ms",  # Naver_Processing_Time
                
                # Comparison Results
                comparison_result.get("similarity_score", 0),  # Similarity_Score
                comparison_result.get("both_successful", False),  # Both_Successful
                comparison_result.get("recommendation", "")  # Recommendation
            ]
            
            print(f"📝 [SHEETS SERVICE] 데이터 길이: {len(row_data)}개 항목")
            
            # 데이터 추가
            if current_row_count == 0:
                # 비어있으면 첫 번째 행에 추가
                worksheet.update('A1', [row_data])
                final_row = 1
                print(f"🎯 [SHEETS SERVICE] 첫 번째 행에 추가 (A1)")
            else:
                # 항상 다음 행에 추가
                next_row = current_row_count + 1
                range_str = f'A{next_row}'
                worksheet.update(range_str, [row_data])
                final_row = next_row
                print(f"🎯 [SHEETS SERVICE] {range_str}에 추가")
            
            # 확인
            final_count = len(worksheet.get_all_values())
            print(f"✅ [SHEETS SERVICE] 저장 완료: {final_row}행 / 총 {final_count}행")
            
            return f"Data added to row {final_row}"
            
        except Exception as e:
            print(f"❌ [SHEETS SERVICE] 저장 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"
    
    def get_spreadsheet_url(self):
        """스프레드시트 URL 반환"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None
    
    def get_analysis_data(self) -> List[Dict]:
        """분석을 위한 데이터 가져오기"""
        worksheet = self.setup_comparison_sheet()
        all_data = worksheet.get_all_records()
        return all_data