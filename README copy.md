
## 📃프로젝트: 희귀질환 정보 검색 사이트
희귀질환 환자 및 보호자들의 정보 검색을 돕고 관련 서비스를 제공하는 웹 사이트 입니다.

### 프로젝트 발표
- [수주제안서](https://drive.google.com/file/d/-1YmUQKVRzeXReqGQ6nQSMrjkwI1SmuzNg/view?usp=drive_link)
- [1차 프로젝트 발표](https://docs.google.com/presentation/d/1YTpxuy2uYwYFA3kO9mQ3rrTPeRXCOuXx8J9yCxwjoxQ/edit#slide=id.p9)
-----
#### <<멤버변경 : 박요한, 김경하, 조유경  -> 조유경, 김하늘, 김덕재, 오지수, 한동철>>
-----
- [1-2차 프로젝트 발표](https://docs.google.com/presentation/d/10ToEiSMfQi9CtyLagILXsOWYHhO6hikPNPoPLa_-MuY/edit)


### ✔️프로젝트 설명
희귀병에 대한 관심 증가와 발전 가능성에 매력을 느꼈음....

### ✔️프로젝트 스케줄링

[Jira_software](https://kdj0712.atlassian.net/jira/software/projects/RDS/boards/3/timeline?selectedIssue=RDS-50)

#### 📌 프로젝트 주요 기능
- 현위치/추천 기반의 의료기관 지도검색
- 증상 별 희귀질환 검색
- 질문, 후기 및 추천글 공유가 가능한 커뮤니티
- 복지, 법체계 변경사항 등 최신동향을 아카이빙한 페이지
- 희귀질환자 대상 프로그램 서비스 페이지 
- 데이터 분석을 기반으로 각 서비스의 의도를 설명하는 회사설명 페이지
- 나의 기록을 저장하는 마이페이지
- 회원을 관리하는 기능의 관리자 페이지

### ✔️개발 기간
총 n개월

- 1차 : 2023.01.08 ~ 2023.01.17
- 2차 : 2023.02.21 ~ 2023.03.20

### ✔️구현 영상

- [1차 프로젝트 결과물](https://www.youtube.com/watch?v=3PTxsHhATEk)
   
### ✔️팀원 및 구현 기능

#### 2차

|카테고리|조유경|김하늘|김덕재|오지수|한동철|
|--|--|--|--|--|--|
|데이터수집|[헬프라인-게시글 데이터 수집(1)](./data/selenium/Helpline.py)[(3)](./data/selenium/helpline_support.py) / [국민청원 데이터 수집](https://github.com/kdj0712/teamKim1/blob/main/data/dummy/%EA%B5%AD%EB%AF%BC%EC%B2%AD%EC%9B%90%20DATA.csv) / [뉴스 데이터 수집](./data/selenium/naver_news_scrapping_healthjosun.py)|[뉴스 데이터 수집](./data/selenium/naver_news_scrapping_yunhab.py)/[rarenote 앱 리뷰 데이터 수집](./data/selenium/rarenote_review.py) |[지식인 데이터 수집(1)](./data/selenium/naver_kin_rare_diseases.py)[(2)](./data/selenium/naver_kin_symptom.py) / [헬프라인-질병정보 데이터 수집(1)](./data/selenium/Helpline_info.py)[(2)](./data/teamplays.diseases.json)[(3)](./data/csv/djkim_helpline_Symptom.csv)|[디시인사이드 게시글 데이터 수집](./data/selenium/dcinside_subfunction.py) / [뉴스 데이터 수집](./data/selenium/naver_news_scrapping_komedi.py)|동철|
|데이터분석|[헬프라인-게시글 자연어 분석](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/Helpline.ipynb)|[뉴스 자연어 분석-타이틀](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/news_rare_disease-title.ipynb) / [뉴스 자연어 분석-전체내용](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/news_rare_disease.ipynb)/ [rarenote 앱 리뷰 자연어 분석](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/sky_rarenote.ipynb)||[디시인사이드 게시글 자연어 분석](https://nbviewer.org/https://github.com/kdj0712/teamKim1/blob/main/data/dcinside.ipynb)/[희귀질환 관련 인구 분석](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/kosis_population.ipynb)|데이터 분석 학습|
|모델링|유경|[뉴스 - 사용자추천 서비스 모델링]()|[헬프라인-질병정보 자연어 기반 모델링](https://nbviewer.org/github/kdj0712/teamKim1/blob/main/data/search_insite_TFIDF.ipynb) /|지수|동철|


<details>
    <summary>pip 등 필요 코드</summary>

#### CLI with Dockerfile and compose.xml : duration 150.4s
```
~$ docker-compose up -d --build

~$ docker-compose build
~$ docker-compose up -d

~$ docker-compose down
~$ docker-compose up -d  # reRunW

설치 불가 시
~$ docker-compose build --no-cache 
~$ docker-compose teamkim1 up -d
```
#### samples
- connect mongodb : [samples\sample_mongodb_connection.ipynb](./samples/sample_mongodb_connection.ipynb)



```
~$ pip install fastapi uvicorn jinja2
~$ pip install python-multipart
~$ pip install beanie
~$ pip install pydantic
~$ pip install pydantic-settings
~$ pip install pydantic[email]
~$ pip install python-dotenv
~$ pip install transformers
~$ pip install torch
~$ pip install tensorflow
~$ pip install --upgrade jupyter ipywidgets
```

for mac
```
~$ pip3 install fastapi uvicorn jinja2
~$ pip3 install python-multipart
~$ pip3 install beanie
~$ pip3 install pydantic
~$ pip3 install pydantic-settings
~$ pip3 install pydantic[email]
~$ pip3 install python-dotenv
~$ pip3 install transformers
~$ pip3 install torch
~$ pip3 install tensorflow
~$ pip3 install --upgrade jupyter ipywidgets
```




</details>





<details>
<summary>프로젝트 1차</summary>

프로젝트명 :RDS
프로젝트 기간: 2023.01.08~2023.01.17

||이름|담당|
|--|--|--|
|1|박요한|PM|
|2|조유경|만능|
|3|김경하|만능|


## 마일스톤
|시작날짜|업무|기간|완료여부|
|--|--|--|--|
|01.10|기획 1차 종합|1d|완|
||업무 분장|당일|완|
|01.11|페이지 프론트 기본 틀 제작|2d|완|
||벡엔드 구상|1d|완|
|01.12|로그인페이지 기본잡기|1d|완|
||로그인 데이터베이스 테스트|1d|완|
||프론트, 데이터베이스 연결 및 확인|1d|완|
|01.13|[질병 데이터 크롤링 제작](https://github.com/entangelk/study_gatheringdatas/blob/main/docs/selenium/disease_save.py)|1d|완|
|01.14|데이터 베이스 더미 제작 및 점검|1d|완|
|01.15|질병 검색 페이지 제작|2d|완|
||페이지네이션 적용|1d|완|
||질병 검색 페이지 데이터베이스 연결|1d|완|
|01.16|유저 데이터베이스, 로그인 회원가입 연결|2d|완|
|01.17|최종 확인(테스트 케이스 작성)|1d||
||각종 문서 작업|1d||



## 주요 파일 리스트
### html
|구분|위치|설명|비고|
|--|--|--|--|
|user|[mainpage.html](./templates/mainpage.html)|메인페이지||
||[login.html](./templates/user/user_login.html)|로그인|ID,PW 유효성 포함|
||[join.html](./templates/user/user_join.html)|회원가입|ID,email 유효성 포함|
||[infosearch.html](./templates/user/user_infosearch.html)|회원정보찾기|email 유효성 포함|
||[privacypolicy.html](./templates/user/user_privacypolicy.html)|약관페이지||
|search|[raredisease.html](./templates/search/search_raredisease.html)|희귀질환 리스트||
|other|[FAQ.html](./templates/other/other_FAQ.html)|FAQ||
||[QnA.html](./templates/other/other_QnA.html)|QnA|게시글 읽기, 쓰기|
|manag|[manager.html](./templates/manag/manag_manager.html)|관리자 페에지|QnA 댓글 작성, 삭제|

### py
|구분|위치|설명|비고|
|--|--|--|--|
|라우트|[mainpage.py](./mainpage.py)|메인페이지 라우트||
||[user.py](./route/user.py)|user하위 라우트||
||[search.py](./route/search.py)|정보찾기 하위 라우트||
||[manag.py](./route/manag.py)|관리자 하위 라우트||
||[other.py](./route/other.py)|기타 하위 라우트||
|컨넥터|[connection.py](./database/connection.py)|서버 컨넥터||
|모델|[member.py](./models/member.py)|user 스키마 모델||
||[QnA.py](./route/QnA.py)|QnA 스키마 모델||
||[FAQ.py](./route/FAQ.py)|FAQ 스키마 모델||
||[disease.py](./route/disease.py)|질병정보 스키마 모델||



</details>









