import os
from datetime import datetime
from pytz import timezone
from github import Github
import requests

def get_event():
    API_PATH = os.environ['REAL_API']
    response = requests.get(API_PATH)
    if response.status_code != 200:
        return ""
    return response.text


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "Dev-Event-Subscribe"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    now_month = int(today.strftime('%m'))
    now_day = int(today.strftime('%d'))
    week = int(now_day/7) + 1
    
    today_int = int(today.strftime('%m%d'))
    
    title = f"주간 Dev Event - {now_month}월 {week}째주 개발자 행사"
    
    content = get_event()
    if content != "":
        # repo에 접근
        g = Github(access_token)
        repo = g.get_organization("brave-people").get_repo(repository_name)
        
        # 이슈 생성
        repo.create_issue(title=title, body=content)
        
        print("issue 등록 완료")
