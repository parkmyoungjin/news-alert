import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import urllib.parse

# 카카오 앱 정보 설정 (여기에 발급받은 REST API 키를 입력하세요)
REST_API_KEY = "bc4bf196268c7a9cc1dd916be6540cca"
REDIRECT_URI = "http://localhost:8000"

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 인증 코드 추출
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')  # UTF-8 인코딩 명시
        self.end_headers()
        
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            code = params['code'][0]
            self.wfile.write('<h1>인증 성공! 이 창을 닫아도 됩니다.</h1>'.encode('utf-8'))  # UTF-8 인코딩 명시
            
            # 토큰 발급 요청
            token_url = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": REST_API_KEY,
                "redirect_uri": REDIRECT_URI,
                "code": code
            }
            
            response = requests.post(token_url, data=data)
            tokens = response.json()
            
            # 토큰 저장
            with open("kakao_token.json", "w", encoding='utf-8') as f:  # UTF-8 인코딩 명시
                json.dump(tokens, f, ensure_ascii=False)  # 한글 깨짐 방지
            
            print("토큰이 성공적으로 발급되어 kakao_token.json 파일에 저장되었습니다.")
            self.server.token_received = True
        else:
            self.wfile.write('<h1>인증 실패...</h1>'.encode('utf-8'))  # UTF-8 인코딩 명시

def get_kakao_token():
    # 카카오 인증 URL 생성 (scope 파라미터 추가)
    auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&scope=talk_message"
    
    # 웹 브라우저로 인증 페이지 열기
    print("카카오 로그인 페이지가 열립니다. 로그인 후 동의하기를 눌러주세요.")
    webbrowser.open(auth_url)
    
    # HTTP 서버 시작하여 인증 코드 받기
    server = HTTPServer(('localhost', 8000), AuthHandler)
    server.token_received = False
    
    # 토큰을 받을 때까지 서버 실행
    while not server.token_received:
        server.handle_request()

if __name__ == "__main__":
    get_kakao_token()