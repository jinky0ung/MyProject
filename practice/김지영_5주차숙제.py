import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbspartaji                      # 'dbspartaji'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190909',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select('#assistant > div:nth-child(1) > ul li')
rank = 1
for movie in movies:
    a_tag = movie.select_one('a')
    if a_tag is not None:
        title1 = a_tag.get('title')
        doc = {
            'category': '영화 인기검색어',
            'rank': rank,
            'title': title1
        }
        db.hw5_movies.insert_one(doc)
        rank += 1

actors = soup.select('#assistant > div:nth-child(2) > ul li')
rank = 1
for actor in actors:
    a_tag = actor.select_one('a')
    if a_tag is not None:
        title2 = a_tag.get('title')
        doc = {
            'category': '영화인 인기검색어',
            'rank': rank,
            'title': title2
        }
        db.hw5_movies.insert_one(doc)
        rank += 1

tickets = soup.select('#reserveRanking0 > ul li')
rank = 1
for ticket in tickets:
    a_tag = ticket.select_one('a')
    if a_tag is not None:
        title3 = a_tag.get('title')
    percent = ticket.select_one('span.ratio').text
    doc = {
        'category': '티켓예매순',
        'rank': rank,
        'title': title3,
        '예매율': percent
    }
    db.hw5_movies.insert_one(doc)
    rank += 1

boxes = soup.select('#assistant > div:nth-child(4) > ul li')
rank = 1
for box in boxes:
    a_tag = box.select_one('a')
    if a_tag is not None:
        title4 = a_tag.get('title')
    num_people = box.select_one('span.ratio').text
    doc = {
        'category': '박스오피스',
        'rank': rank,
        'title': title4,
        '관객수': num_people
    }
    db.hw5_movies.insert_one(doc)
    rank += 1