# 뉴스 알림 카카오톡 서비스

매시간 최신 뉴스를 수집하여 카카오톡으로 발송하는 자동화 서비스입니다.

## 주요 기능

- 네이버 검색 API를 통한 미국 주식시장 및 한국 의료계 뉴스 수집
- 뉴스 기사 본문 추출 및 요약
- 카카오톡을 통한 뉴스 알림 전송
- 뉴스 내용을 깔끔하게 표시하는 웹 페이지 제공
- 오전 8시부터 오후 5시까지 매시간 자동 실행

## 설치 및 설정

### 필수 요구사항

- Python 3.6 이상
- 네이버 개발자 API 키
- 카카오 개발자 API 키

### 설치 방법

```bash
# 필요한 패키지 설치
pip install -r requirements.txt
```

### 초기 설정

1. 카카오 개발자 센터에서 애플리케이션 등록 및 API 키 발급
2. `kakao_auth.py` 파일의 REST_API_KEY 값을 발급받은 키로 변경
3. `kakao_auth.py` 실행하여 토큰 발급
   ```bash
   python kakao_auth.py
   ```
4. 웹 브라우저에서 카카오 계정으로 로그인하고 권한 허용
5. `kakao_message.py` 파일의 server_url 변수를 실제 서버 IP로 업데이트

### Google Cloud VM에서 실행하기

1. 방화벽 설정에서 8080 포트 개방
2. systemd 서비스 등록
   ```bash
   sudo nano /etc/systemd/system/news-service.service

   # 다음 내용 입력
   [Unit]
   Description=News Crawler and Sender Service
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/news-kakao
   ExecStart=/usr/bin/python3 /home/ubuntu/news-kakao/news_scheduler.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
3. 서비스 활성화 및 시작
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable news-service
   sudo systemctl start news-service
   ```

## 주요 파일 설명

- `kakao_auth.py`: 카카오톡 메시지 API 인증 및 토큰 발급
- `kakao_message.py`: 카카오톡으로 뉴스 메시지 전송
- `news_crawler.py`: 네이버 API를 통한 뉴스 수집 및 요약
- `news_scheduler.py`: 정해진 시간에 뉴스를 수집하고 전송하는 스케줄러
- `web_server.py`: 뉴스 웹 페이지 제공을 위한 웹 서버
- `index.html`: 뉴스를 예쁘게 표시하는 웹 페이지

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 