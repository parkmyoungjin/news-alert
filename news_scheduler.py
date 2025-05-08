import schedule
import time
import threading
from datetime import datetime
from news_crawler import get_stock_news, get_medical_news
from kakao_message import send_kakao_message
from web_server import start_web_server

def daily_news_alert():
    """
    일일 뉴스 알림 함수
    """
    today = datetime.now().strftime("%Y년 %m월 %d일")
    current_hour = datetime.now().strftime("%H시")
    print(f"\n===== {today} {current_hour} 뉴스 알림 시작 =====")
    
    # SSL 경고 메시지 비활성화
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 미국 주식 뉴스
    stock_news = get_stock_news()
    if stock_news:
        print("\n===== 오늘의 미국 주식 뉴스 =====")
        for idx, item in enumerate(stock_news, 1):
            print(f"{idx}. {item['title']}")
            if 'summary' in item:
                print(f"   요약: {item['summary'][:50]}...")
            else:
                print("   요약 필드가 없습니다!")
            print(f"   링크: {item['link']}")
            print()
        
        # 디버깅: 첫 번째 뉴스 항목의 키 확인
        first_news = stock_news[0]
        print("첫 번째 뉴스 항목의 키:", list(first_news.keys()))
        
        # 카카오톡으로 발송
        send_kakao_message(stock_news, f"미국 주식시장 ({current_hour})")
    else:
        print("미국 주식 뉴스를 가져오지 못했습니다.")
    
    # 의료계 뉴스
    medical_news = get_medical_news()
    if medical_news:
        print("\n===== 오늘의 의료계 뉴스 =====")
        for idx, item in enumerate(medical_news, 1):
            print(f"{idx}. {item['title']}")
            if 'summary' in item:
                print(f"   요약: {item['summary'][:50]}...")
            else:
                print("   요약 필드가 없습니다!")
            print(f"   링크: {item['link']}")
            print()
        
        # 디버깅: 첫 번째 뉴스 항목의 키 확인
        first_news = medical_news[0]
        print("첫 번째 뉴스 항목의 키:", list(first_news.keys()))
        
        # 카카오톡으로 발송
        send_kakao_message(medical_news, f"한국 의료계 ({current_hour})")
    else:
        print("의료계 뉴스를 가져오지 못했습니다.")
    
    print("===== 뉴스 알림 완료 =====")

def start_web_server_thread():
    """웹 서버를 별도 스레드에서 실행하는 함수"""
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    print("웹 서버가 백그라운드에서 시작되었습니다.")

if __name__ == "__main__":
    # 웹 서버 시작 (별도 스레드에서 실행)
    start_web_server_thread()
    
    # 스케줄 설정 - 오전 8시부터 오후 5시까지 1시간 간격으로 실행
    schedule.every().day.at("08:00").do(daily_news_alert)
    schedule.every().day.at("09:00").do(daily_news_alert)
    schedule.every().day.at("10:00").do(daily_news_alert)
    schedule.every().day.at("11:00").do(daily_news_alert)
    schedule.every().day.at("12:00").do(daily_news_alert)
    schedule.every().day.at("13:00").do(daily_news_alert)
    schedule.every().day.at("14:00").do(daily_news_alert)
    schedule.every().day.at("15:00").do(daily_news_alert)
    schedule.every().day.at("16:00").do(daily_news_alert)
    schedule.every().day.at("17:00").do(daily_news_alert)
    
    # 시작 메시지 출력
    start_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
    print(f"뉴스 알림 스케줄러가 시작되었습니다. ({start_time})")
    print("오전 8시부터 오후 5시까지 1시간 간격으로 알림이 전송됩니다.")
    print("웹 서버는 포트 8080에서 실행 중입니다.")
    print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
    
    # 시작 즉시 알림 전송
    print("\n프로그램 시작과 함께 뉴스 알림을 전송합니다...")
    daily_news_alert()
    
    # 스케줄 실행
    while True:
        schedule.run_pending()
        time.sleep(1)