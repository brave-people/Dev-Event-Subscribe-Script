import requests
import os

from bs4 import BeautifulSoup

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
    """
    event_body = event.findAll("li")
    event_title = event.find("strong")
    
    # link 추출 / 2월과 3월이 다름
    if len(event_body) == 3:
        link = event_title.select("a")[0].attrs['href']
    elif len(event_body) == 4:
        link = event_body[3].select("a")[0].attrs['href']
    else:
        link = "."
        
    date = event_body[2].text
    host = event_body[1].text
    due = find_due_day(event_body[2])[2]
    
    return [event_title.text, link, date, host, due]
    

def content_list(script_title, script_body, events, day):
    """
    event 데이터를 추출, issue의 Body로 정리함.
    param events -> 이벤트의 리스트, 쓰레기 데이터가 존재함. / soup Object List
    param day -> 오늘 날짜. 마감된 날짜를 제거하는 기준이 됨. / int
    
    return str
    """
    current_content = f"## {script_title}\n### {script_body}\n\n" # output

    for event in events:
        if len(event.findAll("li")) > 0: # 내용이 존재하는 Object만 연산
            event_arr = get_event_script(event)
            if day <= int(event_arr[4]):
                content = f"[{event_arr[0]}]({event_arr[1]})" + "\n -" + event_arr[2] + "\n -"+ event_arr[3] + " <br/>\n "
                current_content += content
                
    return current_content
                
def __main__():
    url = 'https://github.com/brave-people/Dev-Event'
    date_now = 210 # 지금 날짜 int형으로
    html = get_html(url)
    event = split_event_html(html)
    
    script_title = "Dev-Event"
    script_body = "이벤트 알려드립니다."
    
    print(content_list(script_title, script_body, event, date_now))

if __name__ == '__main__':
    __main__()