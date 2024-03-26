#웹 스크래핑
#박스오피스 제목으로 상세정보(장르, 감독, 주연배우, 시리즈, 각본가, 원작자, 평점, 평점 참여자수)를 웹 스크래핑하여 info.csv에 저장
import csv
import requests
from bs4 import BeautifulSoup

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    movie_Nm=[]
    for row in reader:
        movie_Nm.append(row['제목'])

result = {}

for name in movie_Nm:
    movieNm = name

    url = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={movieNm}'
    web_data = requests.get(url).text
    
    soup = BeautifulSoup(web_data, "html5lib")
    print(soup)
