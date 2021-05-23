import os
from datetime import datetime
from pytz import timezone
from github import Github

from event_crawling import get_html, split_event_html, content_list


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "Dev-Event-Subscribe"
    event_url = 'https://github.com/brave-people/Dev-Event'
    
    # 스크립트 상단에 소개 및 공지문구
    # markdown 형식으로 적어주세요.
    script_title = '<div align=center> <img src="https://github.com/brave-people/Dev-Event/blob/master/static/title-v3-md.png?raw=true"> \n \n __더 많은 행사를 보고 싶다면? [Github Dev Event](https://github.com/brave-people/Dev-Event) 로 오세요!__ </div>'

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    now_month = int(today.strftime('%m'))
    now_day = int(today.strftime('%d'))
    week = int(now_day/7) + 1
    
    today_int = int(today.strftime('%m%d'))
    
    event_html = get_html(event_url)
    event_object = split_event_html(event_html)
    
    title = f"주간 Dev Event - {now_month}월 {week}째주 개발자 행사"
    
    content = content_list(script_title, event_object, today_int)
    
    # repo에 접근
    g = Github(access_token)
    repo = g.get_organization("brave-people").get_repo(repository_name)
    
    repo.create_issue(title=title, body=content)
    
    print("Update 완료")
