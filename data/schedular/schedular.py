from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger

# 정의한 함수 불러오기
from news_scrappnig_daily import bosascrapping
from news_recommend import update_news_trend_collection

if __name__ == "__main__" : 
    schedular = BackgroundScheduler()

    # news scrapping
    schedular.add_job(bosascrapping,args=["http://www.bosa.co.kr/", "희귀질환"] , trigger="interval", seconds=604800) #주기 설정 필요
    chained_trigger = AndTrigger(trigger1=bosascrapping, trigger2='date', job_id='update_job')
    schedular.add_job(update_news_trend_collection, trigger= chained_trigger)
    schedular.start()

    # word cloud 일주일 단위로 만들기
    


