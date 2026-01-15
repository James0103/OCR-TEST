import requests
import base64
import json
import uuid
import time
from typing import Dict, Any
from app.core.config import settings

class ClovaOCRService:
    def __init__(self):
        self.secret_key = settings.NCP_SECRET_KEY
        self.api_url = settings.NCP_OCR_URL
    
    async def extract_text(self, image_content: bytes) -> Dict[str, Any]:
        import time
        start_time = time.time()
        
        try:
            # 이미지를 base64로 인코딩
            image_base64 = base64.b64encode(image_content).decode('utf-8')
            
            # 요청 데이터 구성
            request_json = {
                'images': [
                    {
                        'format': 'png',
                        'name': 'sample_image',
                        'data': image_base64
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time() * 1000))
            }
            
            # 헤더 설정
            headers = {
                'X-OCR-SECRET': self.secret_key,
                'Content-Type': 'application/json'
            }
            
            # API 요청
            response = requests.post(
                self.api_url,
                data=json.dumps(request_json),
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                images = result.get('images', [])
                
                if images and images[0].get('fields'):
                    full_text = ' '.join([
                        field.get('inferText', '') 
                        for field in images[0]['fields']
                    ])
                    
                    end_time = time.time()
                    process_time = round((end_time - start_time) * 1000, 2)  # ms 단위
                    
                    return {
                        "provider": "naver_clova",
                        "success": True,
                        "full_text": full_text,
                        "process_time": process_time,
                        "error": None
                    }
                else:
                    end_time = time.time()
                    process_time = round((end_time - start_time) * 1000, 2)
                    
                    return {
                        "provider": "naver_clova",
                        "success": False,
                        "full_text": "",
                        "process_time": process_time,
                        "error": "No text detected"
                    }
            else:
                end_time = time.time()
                process_time = round((end_time - start_time) * 1000, 2)
                
                return {
                    "provider": "naver_clova",
                    "success": False,
                    "full_text": "",
                    "process_time": process_time,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            end_time = time.time()
            process_time = round((end_time - start_time) * 1000, 2)
            
            return {
                "provider": "naver_clova",
                "success": False,
                "full_text": "",
                "process_time": process_time,
                "error": str(e)
            }