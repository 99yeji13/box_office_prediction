#영화진흥위원회 OPEN API 이용
#박스오피스 영화코드를 이용해 영화정보(개봉일, 상영시간, 관람등급, 국가)를 movie.csv에 저장
import requests
import json
import csv
from pprint import pprint

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
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
    api_data = requests.get(url).json()

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
    
    