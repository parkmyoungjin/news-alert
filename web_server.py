import http.server
import socketserver
import json
import urllib.parse
import os
from datetime import datetime

# 웹 서버 포트 설정
PORT = 8080

class NewsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # URL 경로 분석
        if self.path == '/':
            # 기본 index.html 제공
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.startswith('/news'):
            # /news 경로에서 뉴스 데이터를 JSON으로 제공
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            topic = params.get('topic', [''])[0]
            news_json = params.get('data', [''])[0]
            
            try:
                # URL 인코딩된 JSON 데이터 디코딩
                if news_json:
                    news_data = json.loads(urllib.parse.unquote(news_json))
                else:
                    news_data = []
                
                # 뉴스 데이터를 구조화된 JSON으로 준비
                response_data = {
                    'stock': [],
                    'medical': []
                }
                
                if topic == '미국 주식시장':
                    response_data['stock'] = news_data
                elif topic == '한국 의료계':
                    response_data['medical'] = news_data
                
                # JSON 응답 전송
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
                
            except Exception as e:
                print(f"오류 발생: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"오류 발생: {e}".encode('utf-8'))
                return
                
        elif self.path.startswith('/view'):
            # /view 경로에서 뉴스 보기 페이지 제공
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            topic = params.get('topic', [''])[0]
            news_json = params.get('data', [''])[0]
            
            # index.html 파일 읽기
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 데이터 파라미터 추가
                if news_json:
                    # index.html을 그대로 제공 (JavaScript에서 URL 파라미터 처리)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write("뉴스 데이터가 없습니다.".encode('utf-8'))
            except Exception as e:
                print(f"오류 발생: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"오류 발생: {e}".encode('utf-8'))
            return
        else:
            # 기본 파일 제공
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def start_web_server():
    # 모든 IP에서의 접속 허용 (0.0.0.0)
    with socketserver.TCPServer(("0.0.0.0", PORT), NewsHandler) as httpd:
        print(f"웹 서버가 포트 {PORT}에서 시작되었습니다.")
        print(f"모든 IP에서 접속 가능합니다.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("웹 서버를 종료합니다.")
            httpd.shutdown()

if __name__ == "__main__":
    start_web_server() 