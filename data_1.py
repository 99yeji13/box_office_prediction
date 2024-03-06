#50주간의 박스오피스 데이터(영화코드, 영화명, 누적관객수)를 저장하여 boxoffice.csv파일에 저장
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

result = {}

with open('config.json') as f:
    config = json.load(f)

#2024년 3월 1일 기준으로 과거 50주간의 데이터를 뽑아오기
#주간(월~일)까지 데이터 조회 weekGb=0
#다양한 영화/상업 영화 모두 포함. 한국/외국 영화 모두 포함. 모든 상영지역 포함.
for i in range(50):
  key = config['KEY']
  targetDt = datetime(2024,3,1) - timedelta(weeks=i)
  targetDt = targetDt.strftime('%Y%m%d') #20240301 형식으로 변환

  url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={key}&targetDt={targetDt}&weekGb=0'
  api_data = requests.get(url).json()
  
  #주간/주말 박스오피스 데이터 리스트로 가져오기.
  movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
  
  for movie in movies:
      code = movie.get("movieCd")
      if code not in result:
          result[code] = {
              'id' : movie.get("movieCd"),
              'title' : movie.get("movieNm"),
              'release_date' : movie.get("openDt"),
              'audience': movie.get("audiAcc")
          }