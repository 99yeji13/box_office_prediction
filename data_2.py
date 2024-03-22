#네이버 웹 크롤링(스크래핑)
#boxoffice.csv 파일의 영화제목으
import requests
import json
import csv
from pprint import pprint

# 1 csv.DictReader() _ boxoffice에서 영화제목 읽어오기
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력 => reader에 파일이 들어있음
    # 한 줄씩 읽는다.
    movie_Cd=[]
    for row in reader:
        movie_Cd.append(row['영화대표코드'])

result = {}

with open('config.json') as f:
    config = json.load(f)
    
for code in movie_Cd:
    key = config['KEY']
    movieCd = code

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'
    api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌

    movies_info = api_data.get('movieInfoResult').get('movieInfo')
    
    for info in movies_info:
            code = movies_info.get('movieCd')

            result[code] = {
                    '영화대표코드': movies_info.get('movieCd'),
                    '개봉일': movies_info.get('openDt'),
                    '상영시간': movies_info.get('showTm'),
                    '관람등급': movies_info.get('audits')[0].get('watchGradeNm') if movies_info.get('audits') else None,
                    '국가': movies_info.get("nations")[0].get("nationNm")
                }
        
with open('movie.csv', 'w', encoding = 'utf-8', newline = '') as f:
    fieldnames = ('영화대표코드', '개봉일', '상영시간', '관람등급', '국가')
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for value in result.values():
        writer.writerow(value)
    
    