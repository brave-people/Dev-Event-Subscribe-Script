import requests
import os

from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def get_html(url) -> str:
    """
    url에 해당되는 html을 str으로 가져옴
    param url -> 가져 올 url / str
    return str
    """
    response = requests.get(url)
    return response.text

def split_event_html(html, range = 20):
    """    
    html 중 이벤트 부분을 찾아서 반환
    두달치로 고정
    param html -> 페이지의 html / str
    param range -> event의 위치 / int
    return soup Object List
    """
    br_split_HTML = list(html.split('<br>')[range:])
    soup = BeautifulSoup(br_split_HTML[0] + br_split_HTML[1], 'html.parser')
    return soup.findAll("li")

def find_due_day(body):
    """
    이벤트에서 마감일자를 찾아줌
    param body -> 이벤트 날짜 / soup Object
    return -> arr
    arr[0] = month
    arr[1] = date
    arr[2] = month&date
    """
    str_body = str(body)
    dot_split_str = str_body.split('.')
    """
    expected
    '<li>신청: 02', ' 04(목) 14:00 / 02', ' 05(금) 14:00</li>'
    """
    month = dot_split_str[-2][-2:]
    day = dot_split_str[-1][1:3]
    MnD = month + day
    return [month,day,MnD]

def content_list(events, day):
    """
    event 데이터를 추출, issue의 Body로 정리함.
    param events -> 이벤트의 리스트, 쓰레기 데이터가 존재함. / soup Object List
    param day -> 오늘 날짜. 마감된 날짜를 제거하는 기준이 됨. / int
    
    return str
    """
    current_content = '' # output
    
    for event in events:
        event_body = event.findAll("li")
        event_title = event.find("strong")
        
        if len(event_body) > 0: # 내용이 존재하는 Object만 연산
            link = event_body[3].select("a")[0].attrs['href']
            due_date = find_due_day(event_body[2])
            if day <= int(due_date[2]):
                content = f"[{event_title.text}]({link})" + "\n -" + event_body[2].text + "\n -"+ event_body[1].text + " <br/>\n "
                current_content += content