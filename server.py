# 패키지설치: requests, flask, pymongo, beautifulsoup4
import requests  # url로 요청을 보낼 때 사용하는 친구
import openpyxl
from bs4 import BeautifulSoup  # 크롤링, HTML을 찾기 쉽게 만들어주는 친구
from flask import Flask  # API, HTML 요청을 받았을 때 적절한 결과를 내려주는 친구 (서버 프레임워크)
from flask import render_template  # HTML을 예쁘게 브라우저로 내려주는 친구
from flask import jsonify  # API에 Dictionary를 예쁘게 내려주는 친구
from flask import request  # front에서 요청된 값들을 보관하고 있는 친구
from pymongo import MongoClient  # python에서 몽고 DB에 접속하는 것을 도와주는 친구


client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbbook                        # 'dbbook'라는 이름의 db를 만듭니다.

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# POST 요청은 브라우저에서 URL로만은 못보냄 -> 자바스크립트 Ajax 요청을 통해서만 가능
# localhost:5000/post 라는 url로 POST 요청이 왔을 때


@app.route('/post', methods=['POST'])
def saving():
    # 브라우저(Java Script AJAX)에서 보낸 값들을 변수에 저장한다.
    isbn_receive = request.form['isbn_give']  # 클라이언트로부터 url을 받는 부분
    startdate_receive = request.form['startdate_give']  # 클라이언트로부터 comment를 받는 부분
    enddate_receive = request.form['enddate_give']  # 클라이언트로부터 받은 작가이름
    star_receive = request.form['star_give']
    channel_receive = request.form['channel_give']
    shreview_receive = request.form['shreview_give']
    lgreview_receive = request.form['lgreview_give']

    # header는 requests 라이브러리를 쓸 때, 보내는 사람이 어떤 사람인지 표시 (안중요함)
    #headers = {
    #    'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko)'
    #               'Chrome/73.0.3683.86 Safari/537.36'}
    headers = {
    'Authorization': f'KakaoAK 88b58d8c44794be513f1a1261960236d'
    }
    data = requests.get(f"https://dapi.kakao.com/v3/search/book?&query={isbn}", headers=headers)
    response = data.json()

    #documents의 0번째 리스트에서 책정보를 읽어와서 각 변수에 저장.
    datetime = response['documents'][0]['datetime'].split('T')[0]
    author = response['documents'][0]['translators']
    translator = response['documents'][0]['translators']
    publisher = response['documents'][0]['publisher']
    title = response['documents'][0]['title']
    bookimage = response['documents'][0]['thumbnail']


    #데이터들을 dictionary 형태로 포장 (이유는 쉽게 저장하기 위해)
    bookinfo = dict(isbn=isbn_receive,
                   시작일=startdate_receive,
                   종료일=enddate_receive,
                   나의평점=star_receive,
                   추천경로=channel_receive,
                   한줄리뷰=shreview_receive,
                   나의리뷰=lgreview_receive,
                   발행일=datetime,
                   저자 = author,
                   역자 = translator,
                   출판사 = publisher,
                   책제목 = title,
                   책이미지 = bookimage)

    # article collection에  dictionary를 저장
    db.bookinfos.insert_one(bookinfo)
    return jsonify({'result': 'success'})


# localhost:5000/post 라는 url로 GET 요청이 왔을 때

@app.route('/post', methods=['GET'])
def listing():
    # 모든 article 찾기 & _id 값은 출력에서 제외하기
    result = list(db.bookinfos.find({}, {'_id': 0}))
    # articles라는 키 값으로 영화정보 내려주기
    # jsonify에게 data를 넘겨주기 위해 dictionary 형태로 재가공
    response = {
        'result': 'success',
        'bookinfos': result
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
