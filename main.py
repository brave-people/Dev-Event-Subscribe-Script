import os
from datetime import datetime
from pytz import timezone
from github import Github

from event_crawling import get_html, split_event_html, content_list


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "Dev-Event-Subscribe"
    event_url = 'https://github.com/brave-people/Dev-Event'

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_title = today.strftime("%Y년 %m월 %d일")
    today_int = int(today.strftime('%m%d'))
    
    event_html = get_html(event_url)
    event_object = split_event_html(event_html)
    
    title = f"오늘의 이벤트 - {today_title}"
    
    content = content_list(event_object, today_int)
    
    # repo에 접근
    g = Github(access_token)
    repo = g.get_organization("brave-people").get_repo(repository_name)
    
    repo.create_issue(title=title, body=content)
    
    print("Update 완료")