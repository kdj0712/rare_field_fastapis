# from'https://itunes.apple.com/kr/rss/customerreviews/page={}/id={}/sortby=mostrecent/json'
import requests
import xmltodict
# url 주소 변수 지정
# sickCd = ['M542','S134']
# medTp = 1,2
import time
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003/")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['caregive_platform_apple']
# insert 작업 진행
i = 0
count_reviews = 0
list_app = [1495648148,
1516171776,
1644025883,
1574834462,
6464281234,
1669660886,
1669661012,
1572236177,
6469492370,
6476480122,
1290551764,
6475797861,
1591335130,
1619862367,
6476087739,
1627881998,
6443856022,]
list_app_name = ["케어닥",
"케어네이션",
"케어네이션(간병인용)",
"헬퍼",
"보미쌤(보호자용)",
"토닥씨",
"토닥씨 간병인전용",
"이웃하다",
"케어버디",
"간병 나이팅게일",
"병원잡",
"간병인24",
"또하나의가족",
"시니어 톡톡",
"모시미",
"케어콜",
"헬로우케어"]
for j in  range(len(list_app)):
    i = 0
    while True:
        i += 1
        try:
            url = f'https://itunes.apple.com/kr/rss/customerreviews/page={i}/id={list_app[j]}/sortby=mostrecent/json'
            pass
            # respose라는 변수로 받음
            response = requests.get(url)
            pass
            # response의 내용을 출력
            print(response.content)
            # json 파일을 dictionary 형태로 변환
            import json
            contents = json.loads(response.content)
            for content in contents['feed']['entry']:
                data_dict = {}
                app_name = list_app_name[j]
                user_score = content['im:rating']['label']
                user_date = content['updated']['label']
                user_comments = content['content']['label']
                evaluation = content['im:voteSum']['label']
                data_dict['app_name'] = app_name
                data_dict['user_score'] = user_score
                data_dict['user_date'] = user_date
                data_dict['user_comments'] = user_comments
                data_dict['evaluation'] = evaluation
                print(app_name)
                print(user_score)
                print(user_date)
                print(user_comments)
                print(evaluation)
                count_reviews += 1
                print(count_reviews)
                result = collection.insert_one(data_dict)
        except:
            break
    pass






