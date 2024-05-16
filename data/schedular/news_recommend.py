# 몽고디비 연결
from pymongo import MongoClient
import pickle
import os
from konlpy.tag import Okt

def dbconnect(Database_name, collection_name) :
    mongoClient = MongoClient("mongodb://trainings.iptime.org:45003/")
    database = mongoClient[Database_name]
    collection = database[collection_name]
    return collection

def tokenizer(raw, pos=['Noun', 'Verb']):
    stopword = ['서울대', '희귀질환', '희귀', '대다',  '케다', '소아', '생명', '한국', '한미','사노피', '하다', '급여', '국내', '샤이어',  '스케', '세포'
            , '병원',  '질환',  '한독', '화이자제약',  '전달', '질병', '인하대병원',  '관리', '다국적', '환자', '지정', '치료'
            , '오다', '헌터', '작년', '브리', '위해', '베다', '받다', '심평원', '코로나', '건보', '화순', '전남대', '실시', '자임','녹십자'
            ] #추가 생성 필요
    okt=Okt()
    return [
        word for word, tag in okt.pos(raw, norm=True, stem=True)
        if len(word) >1 and tag in pos and word not in stopword
    ]
    

def update_news_trend_collection():
    news_weekly_collection = dbconnect("teamkim", "news_weekly_thevoice")
    news_collection = dbconnect("teamkim", "trend_news_test")
    
    # daily 에 있는 내용 가지고 오기
    cursor = news_weekly_collection.find({})
    
    file_path = os.path.join(os.getcwd(), 'data', 'pkl', 'news_recommend_vectorizer.pkl')
    with open(file_path, "rb") as file:
        vectorizer = pickle.load(file)

    with open(os.path.join('data', 'pkl', 'news_recommend_model.pkl'), "rb") as file:
        model = pickle.load(file)

    # vectorizer(tokenizer=tokenizer)

    for document in cursor :
        news_title = document.get('news_title')
        news_topic_array = model.predict(vectorizer.transform([news_title]))
        news_topic = ''.join(news_topic_array)
        document['news_topic'] = news_topic
        news_collection.insert_one(document)
        pass

    # news_trend_collection에 내용 추가하기

if __name__ == "__main__" :
    update_news_trend_collection()
    pass