import requests
import os
import re

from bs4 import BeautifulSoup

def get_html(url):
    """
    url에 해당되는 html을 str으로 가져옴
    param url -> 가져 올 url / str
    return str
    """
    response = requests.get(url)
    return response.text

def split_event_html(html):
    """    
    html 중 이벤트 부분을 찾아서 반환
    두달치로 고정
    param html -> 페이지의 html / str
    param range -> event의 위치 / int
    return soup Object List
    """
    split_HTML = list(html.split('<h2')[6:])
    soup = BeautifulSoup(split_HTML[0] + split_HTML[1] + split_HTML[2], 'html.parser')
    return soup.findAll("li")

def find_day_by_body(body):
    """
    이벤트에서 일자를 찾아줌
    param body -> 이벤트 날짜 / soup Object
    return -> arr
    arr[0] = due_day
    arr[1] = start_day
    """

    str_body = str(body)

    dot_split_str = str_body.split('.')
    """
    expected
    '<li>신청: 02', ' 04(목) 14:00 / 02', ' 05(금) 14:00</li>'
    """

    date_len = len(dot_split_str)
    res = ["0", "0"]

    for i in range(date_len - 1):
        res.insert(0, find_day_by_stub(dot_split_str[i], dot_split_str[i+1]))

    return res

def find_day_by_stub(mon_stub, day_stub):
    """
    stub에서 정규표현식을 통해서 정수를 찾아주는 로직
    param -> str, str
    return -> str
    """
    month = get_number_by_string(mon_stub[-3:])
    days = get_number_by_string(day_stub[:3])
    MnD = month + days
    return MnD

def get_number_by_string(str: str):
    return re.findall("\d+", str)[0]

def get_event_script(event):
    """
    event에서 
    param event_body -> event / soup Object
    return arr(str)
    arr[0] = title
    arr[1] = link
    arr[2] = date
    arr[3] = host
    arr[4] = due
    arr[5] = start
    """
    event_body = event.findAll("li")
    event_title = event.find("strong")
    
    # link 추출
    link = event_title.select("a")[0].attrs['href']
        
    date = event_body[2].text
    host = event_body[1].text
    date_info = find_day_by_body(event_body[2])
    due = date_info[0]
    start = date_info[1]
    
    return [event_title.text, link, date, host, due, start]
    

def is_activate_event(first_date, second_date, today) -> bool:
    """
    이벤트가 현재 날짜에 진행되고 있는지를 파악함
    param first_date -> 이벤트의 종료 일자. / string
    param second_date -> 이벤트의 시작 일자. 없다면 '0'이 들어가게 됨. / string
    param today -> 오늘 날짜. 마감된 날짜를 가리는 기준이 됨. / int
    
    return bool
    """
    event_start_date = 0
    event_end_date = int(first_date)

    if second_date == '0':
        event_start_date = int(first_date)
    else:
        event_start_date = int(second_date)
        event_end_date = int(first_date)

        if event_start_date > event_end_date:
            event_end_date += 1200
            today += 1200

    date_range = today + 100

    return (today <= event_end_date) and (date_range >= event_start_date)
    
def content_list(script_title, events, today):
    """
    event 데이터를 추출, issue의 Body로 정리함.
    param events -> 이벤트의 리스트, 쓰레기 데이터가 존재함. / soup Object List
    param day -> 오늘 날짜. 마감된 날짜를 제거하는 기준이 됨. / int
    
    return str
    """
    current_content = f"{script_title} \n \n"

    for event in events:
        if len(event.findAll("li")) > 0: # 내용이 존재하는 Object만 연산
            event_arr = get_event_script(event)
            
            if is_activate_event(event_arr[4], event_arr[5], today):
                content = f"[{event_arr[0]}]({event_arr[1]})" + "\n -" + event_arr[2] + "\n -"+ event_arr[3] + " <br/>\n "
                current_content += content
                
    return current_content
                
def __main__():
    url = 'https://github.com/brave-people/Dev-Event'
    date_now = 206 # 지금 날짜 int형으로
    html = get_html(url)
    event = split_event_html(html)
    
    print(content_list("테스트 공지", event, date_now))
    # print(event)

if __name__ == '__main__':
    __main__()
