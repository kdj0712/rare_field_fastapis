# 일주일 단위로 워드 클라우드 제작을 위한 def 만들기

# terminal에서 설치해야할 것들
# ~$ pip install wordcloud



from pymongo import MongoClient 
import pandas as pd
import numpy as np


## 일단 이 친구도 몽고디비에 연결해야함

def dbconnect(Database_name, collection_name):
    mongoClient = MongoClient("mongodb://trainings.iptime.org:45003/")
    database = mongoClient[Database_name]
    collection = database[collection_name]
    return collection

d