import csv
import json
import requests

with open('boxoffice.csv', newline = '', encoding ='utf-8') as f:
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
                    '영화제목(국문)': movies_info.get('movieNm'),
                    '영화제목(영문)': movies_info.get('movieNmEn'),
                    '영화제목(원문)': movies_info.get('movieNmOg'),
                    '관람등급': movies_info.get('audits')[0].get('watchGradeNm') if movies_info.get('audits') else None,
                    '개봉연도': movies_info.get('openDt'),
                    '상영시간': movies_info.get('showTm'),
                    '장르': movies_info.get('genres')[0].get('genreNm'),
                    '감독': movies_info.get('directors')[0].get('peopleNm') if movies_info.get('directors') else None
            }
        
        
with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('영화대표코드', '영화제목(국문)', '영화제목(영문)', '영화제목(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)