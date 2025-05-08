import requests
from datetime import datetime
import urllib.parse
from newspaper import Article
import traceback

# 네이버 API 키 (개발자 센터에서 발급)
NAVER_CLIENT_ID = "3couAsaovMS4sN_hDybS"
NAVER_CLIENT_SECRET = "w6qZE5Q4ID"

def get_article_summary(url):
    """
    뉴스 기사 URL에서 본문을 추출하고 요약하는 함수
    """
    try:
        # newspaper3k 라이브러리 사용하여 기사 추출
        article = Article(url, language='ko')
        article.download()
        article.parse()
        
        # 본문 추출
        text = article.text
        
        # 본문이 너무 길면 첫 3문장만 사용
        sentences = text.split('.')
        summary = '.'.join(sentences[:3]) + '.'
        
        # 요약이 너무 길면 200자로 제한
        if len(summary) > 200:
            summary = summary[:197] + '...'
            
        return summary
    except Exception as e:
        print(f"기사 요약 중 오류 발생: {e}")
        traceback.print_exc()
        return "기사 요약을 가져올 수 없습니다."

def get_stock_news():
    """미국 주식 관련 뉴스를 가져오는 함수"""
    print("미국 주식 뉴스 요청 중...")
    
    # 네이버 검색 API를 사용하여 미국 주식 관련 뉴스 가져오기
    query = urllib.parse.quote("미국 주식 시장")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # 응답 확인
        if response.status_code != 200:
            print(f"네이버 API 요청 실패: {response.status_code} - {response.text}")
            return get_default_stock_news()  # 실패 시 기본 뉴스 반환
        
        # JSON 형태로 변환
        news_data = response.json()
        
        # 뉴스 목록 추출
        items = news_data.get("items", [])
        print(f"받아온 뉴스 수: {len(items)}")
        
        if not items:
            print("뉴스가 없습니다. 기본 뉴스를 사용합니다.")
            return get_default_stock_news()
        
        # 뉴스 데이터 정리
        news_list = []
        for i, item in enumerate(items):
            # HTML 태그 제거
            title = item.get("title", "제목 없음").replace("<b>", "").replace("</b>", "")
            link = item.get("link", "#")
            
            # 기사 본문 요약
            summary = get_article_summary(link)
            
            news_list.append({
                "title": title,
                "link": link,
                "summary": summary
            })
            print(f"  - 뉴스 {i+1}: {title}")
            print(f"    요약: {summary[:50]}...")
        
        return news_list
        
    except Exception as e:
        print(f"뉴스 가져오기 오류: {e}")
        traceback.print_exc()
        return get_default_stock_news()  # 오류 발생 시 기본 뉴스 반환

def get_medical_news():
    """한국 의료계 관련 뉴스를 가져오는 함수"""
    print("의료계 뉴스 요청 중...")
    
    # 네이버 검색 API를 사용하여 의료 관련 뉴스 가져오기
    query = urllib.parse.quote("의료계")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # 응답 확인
        if response.status_code != 200:
            print(f"네이버 API 요청 실패: {response.status_code} - {response.text}")
            return get_default_medical_news()  # 실패 시 기본 뉴스 반환
        
        # JSON 형태로 변환
        news_data = response.json()
        
        # 뉴스 목록 추출
        items = news_data.get("items", [])
        print(f"받아온 뉴스 수: {len(items)}")
        
        if not items:
            print("뉴스가 없습니다. 기본 뉴스를 사용합니다.")
            return get_default_medical_news()
        
        # 뉴스 데이터 정리
        news_list = []
        for i, item in enumerate(items):
            # HTML 태그 제거
            title = item.get("title", "제목 없음").replace("<b>", "").replace("</b>", "")
            link = item.get("link", "#")
            
            # 기사 본문 요약
            summary = get_article_summary(link)
            
            news_list.append({
                "title": title,
                "link": link,
                "summary": summary
            })
            print(f"  - 뉴스 {i+1}: {title}")
            print(f"    요약: {summary[:50]}...")
        
        return news_list
        
    except Exception as e:
        print(f"뉴스 가져오기 오류: {e}")
        traceback.print_exc()
        return get_default_medical_news()  # 오류 발생 시 기본 뉴스 반환

# API 호출 실패 시 사용할 기본 뉴스
def get_default_stock_news():
    """미국 주식 관련 기본 뉴스를 제공하는 함수"""
    print("미국 주식 기본 뉴스 목록 생성 중...")
    
    # 현재 날짜를 기준으로 테스트 데이터 생성
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    # 정적 뉴스 데이터
    news_list = [
        {
            "title": f"[{today}] 미국 다우지수 상승세 유지, 기술주 강세",
            "link": "https://finance.naver.com",
            "summary": "미국 증시에서 다우지수가 상승세를 유지하고 있으며, 특히 기술주가 강세를 보이고 있습니다. 투자자들은 실적 호조와 경제 지표 개선에 주목하고 있습니다."
        },
        {
            "title": f"[{today}] 연준, 금리 동결 결정... 하반기 금리 인하 전망",
            "link": "https://finance.naver.com",
            "summary": "미 연방준비제도(Fed)가 기준금리를 현행 수준에서 동결하기로 결정했습니다. 연준은 인플레이션이 목표치에 근접함에 따라 하반기에 금리 인하를 검토할 것으로 전망됩니다."
        },
        {
            "title": f"[{today}] 애플·마이크로소프트 실적 발표, 시장 예상치 상회",
            "link": "https://finance.naver.com",
            "summary": "애플과 마이크로소프트가 분기 실적을 발표했으며, 두 기업 모두 시장 예상치를 상회했습니다. 클라우드 서비스와 인공지능 사업 확대가 성장을 이끌었습니다."
        },
        {
            "title": f"[{today}] 미국 금융시장, 인플레이션 우려 완화로 상승",
            "link": "https://finance.naver.com",
            "summary": "미국 금융시장이 인플레이션 우려 완화로 상승세를 보이고 있습니다. 물가 상승률이 둔화되면서 투자자들의 신뢰가 회복되고 있는 추세입니다."
        },
        {
            "title": f"[{today}] 전문가들이 예상하는 하반기 미국 증시 전망",
            "link": "https://finance.naver.com",
            "summary": "금융 전문가들은 하반기 미국 증시에 대해 신중한 낙관론을 제시하고 있습니다. 금리 인하 가능성과 기업 실적 개선이 주가 상승을 견인할 것으로 전망됩니다."
        }
    ]
    
    print(f"미국 주식 기본 뉴스 {len(news_list)}개 생성 완료")
    
    # 생성된 뉴스 데이터 출력
    for idx, news in enumerate(news_list, 1):
        print(f"  - 뉴스 {idx}: {news['title']}")
        print(f"    요약: {news['summary'][:50]}...")
    
    return news_list

def get_default_medical_news():
    """의료계 관련 기본 뉴스를 제공하는 함수"""
    print("의료계 기본 뉴스 목록 생성 중...")
    
    # 현재 날짜를 기준으로 테스트 데이터 생성
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    # 정적 뉴스 데이터
    news_list = [
        {
            "title": f"[{today}] 보건복지부, 의료 인력 확충 계획 발표",
            "link": "https://news.naver.com",
            "summary": "보건복지부가 의료 인력 확충을 위한 중장기 계획을 발표했습니다. 지방 의료기관의 인력난 해소와 전문의 수급 개선이 주요 과제로 설정되었습니다."
        },
        {
            "title": f"[{today}] 코로나19 확진자 감소세, 방역 체계 조정",
            "link": "https://news.naver.com",
            "summary": "코로나19 확진자 수가 지속적인 감소세를 보이는 가운데, 정부가 방역 체계를 조정했습니다. 일상 회복에 중점을 둔 새로운 방역 지침이 마련되었습니다."
        },
        {
            "title": f"[{today}] 신약 개발 투자 늘린다...제약사 연구개발 확대",
            "link": "https://news.naver.com",
            "summary": "국내 제약사들이 신약 개발에 대한 투자를 확대하고 있습니다. 글로벌 경쟁력 강화를 위한 연구개발 중심의 경영 전략을 추진하는 기업이 증가하는 추세입니다."
        },
        {
            "title": f"[{today}] 의사협회, 의료정책 개선 제안서 제출",
            "link": "https://news.naver.com",
            "summary": "대한의사협회가 정부에 의료정책 개선 제안서를 제출했습니다. 의료 수가 현실화와 의료 환경 개선을 위한 다양한 정책적 대안이 포함되어 있습니다."
        },
        {
            "title": f"[{today}] 디지털 헬스케어 시장 급성장...원격진료 확대",
            "link": "https://news.naver.com",
            "summary": "디지털 헬스케어 시장이 급성장하고 있으며, 특히 원격진료 서비스가 확대되고 있습니다. 인공지능과 빅데이터를 활용한 건강관리 솔루션 개발이 활발히 이루어지고 있습니다."
        }
    ]
    
    print(f"의료계 기본 뉴스 {len(news_list)}개 생성 완료")
    
    # 생성된 뉴스 데이터 출력
    for idx, news in enumerate(news_list, 1):
        print(f"  - 뉴스 {idx}: {news['title']}")
        print(f"    요약: {news['summary'][:50]}...")
    
    return news_list

# 테스트 코드
if __name__ == "__main__":
    print(f"현재 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}")
    
    print("\n미국 주식 뉴스 테스트 시작...")
    stock_news = get_stock_news()
    print(f"가져온 주식 뉴스 수: {len(stock_news)}")
    for idx, news in enumerate(stock_news, 1):
        print(f"{idx}. {news['title']}")
        print(f"   요약: {news['summary']}")
        print(f"   링크: {news['link']}")
        print()
    
    print("\n의료계 뉴스 테스트 시작...")
    medical_news = get_medical_news()
    print(f"가져온 의료 뉴스 수: {len(medical_news)}")
    for idx, news in enumerate(medical_news, 1):
        print(f"{idx}. {news['title']}")
        print(f"   요약: {news['summary']}")
        print(f"   링크: {news['link']}")
        print()