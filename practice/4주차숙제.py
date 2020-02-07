import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.geniechart                    # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

rank = 1
for song in songs:
    a_tag = song.select_one('td.info > a.title.ellipsis')

    if a_tag is not None:
        title = song.select_one('td.info > a.title.ellipsis').text
        short_title = title.strip()
        singer = song.select_one('td.info > a.artist.ellipsis').text
        #print (rank,short_title,singer)
        doc = {
            'rank': rank,
            'title': short_title,
            'singer': singer
        }
        db.songs.insert_one(doc)
        rank += 1

