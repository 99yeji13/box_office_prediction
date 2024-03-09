#50주간의 박스오피스 데이터(영화코드, 영화명, 누적관객수)를 저장하여 boxoffice.csv파일에 저장하기
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import csv

result = {}

with open('config.json') as f:
    config = json.load(f)

#2024년 3월 1일 기준으로 과거 50주간의 데이터를 뽑아오기
#주간(월~일)까지 데이터 조회 weekGb=0
#다양한 영화/상업 영화. 한국/외국 영화. 모든 상영지역.
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
      #날짜를 거꾸로 돌아가면서 데이터를 얻는다.
      #이미 영화코드가 들어가있다면 그게 마지막 주 자료며, 딕셔너리에 넣지 않는다.
      if code not in result:
          #영화코드명을 key로 가지는 딕셔너리 내부에 필요한 정보들(영화코드, 제목, 개봉일, 관중수)을 가지는 딕셔너리를 생성하기
          result[code] = {
              '코드' : movie.get("movieCd"),
              '제목' : movie.get("movieNm"),
              '개봉일' : movie.get("openDt"),
              '관중수': movie.get("audiAcc")
          }
          
with open('boxoffice.csv', 'w', encoding = 'utf-8', newline = '') as f:
    fieldnames = ('movieCd', 'movieNm', 'openDt', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for value in result.values():
        writer.writerow(value)