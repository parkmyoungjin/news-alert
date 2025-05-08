import json
import requests
import urllib.parse
from datetime import datetime

def send_kakao_message(news_data, topic_name):
    """
    카카오톡으로 뉴스를 발송하는 함수
    """
    # 토큰 불러오기
    try:
        with open("kakao_token.json", "r") as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print("카카오톡 토큰 파일(kakao_token.json)이 없습니다.")
        print("먼저 kakao_auth.py를 실행하여 토큰을 발급받으세요.")
        return False
    
    # 현재 날짜
    today = datetime.now().strftime("%Y년 %m월 %d일")
    current_hour = datetime.now().strftime("%H시")
    
    # 메시지 텍스트 구성
    text = f"[{today} {current_hour} {topic_name} 뉴스]\n\n"
    for idx, news in enumerate(news_data, 1):
        text += f"{idx}. {news['title']}\n"
        if 'summary' in news and len(news['summary']) > 0:
            summary_preview = news['summary'][:30] + "..." if len(news['summary']) > 30 else news['summary']
            text += f"요약: {summary_preview}\n"
        text += f"링크: {news['link']}\n\n"
    
    # 뉴스 데이터를 URL 파라미터로 인코딩
    encoded_news_data = urllib.parse.quote(json.dumps(news_data))
    
    # 웹 서버 URL - VM의 외부 IP 주소를 여기에 입력하세요
    # 예: server_url = "http://34.123.123.123:8080"
    server_url = "http://34.64.136.183:8080"  # 실제 VM IP로 변경
    view_url = f"{server_url}/view?topic={urllib.parse.quote(topic_name)}&data={encoded_news_data}"
    
    # 메시지 보내기
    header = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": view_url,
                "mobile_web_url": view_url
            },
            "button_title": "자세히 보기"
        })
    }
    
    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=header,
        data=data
    )
    
    if response.status_code == 200:
        print(f"{topic_name} 뉴스가 카카오톡으로 발송되었습니다.")
        print(f"자세히 보기 URL: {view_url}")
        return True
    else:
        print(f"메시지 발송 실패: {response.text}")
        return False

# 테스트 용도
if __name__ == "__main__":
    # 테스트 데이터
    test_news = [
        {
            "title": "테스트 뉴스 1", 
            "link": "https://example.com/1",
            "summary": "이것은 테스트 뉴스 1의 요약입니다. 실제 뉴스 내용이 여기에 요약되어 표시됩니다."
        },
        {
            "title": "테스트 뉴스 2", 
            "link": "https://example.com/2",
            "summary": "이것은 테스트 뉴스 2의 요약입니다. 실제 뉴스 내용이 여기에 요약되어 표시됩니다."
        }
    ]
    
    send_kakao_message(test_news, "테스트")