import yfinance as yf

# 금 선물 티커: GC=F
gold_ticker = yf.Ticker("GC=F")

# 최근 1년간 일별 금 시세 데이터 가져오기
gold_data = gold_ticker.history(period="1y")

# 데이터 출력
print(gold_data)
print(gold_data.columns)

# 'Close' 컬럼만 선택
close_data = gold_data['Close']
print(close_data)

# 금에 대한 기본 정보 및 통계
gold_info = gold_ticker.info
print(gold_info)