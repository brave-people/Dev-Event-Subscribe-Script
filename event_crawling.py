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

def split_event_html(html):
    """    
    html 중 이벤트 부분을 찾아서 반환
    두달치로 고정
    param html -> 페이지의 html / str
    param range -> event의 위치 / int
    return soup Object List
    """
    split_HTML = list(html.split('<h2>')[7:])
    soup = BeautifulSoup(split_HTML[0] + split_HTML[1], 'html.parser')
    return soup.findAll("li")

def find_due_day(body):
    """
    이벤트에서 마감일자를 찾아줌
    param body -> 이벤트 날짜 / soup Object
    return -> arr
    arr[0] = month
    arr[1] = date
    arr[2] = month&date
    arr[3] = start_day
    """
    str_body = str(body)
    dot_split_str = str_body.split('.')
    """
    expected
    '<li>신청: 02', ' 04(목) 14:00 / 02', ' 05(금) 14:00</li>'
    """
    try:
        month = dot_split_str[-2][-2:]
        day = dot_split_str[-1][1:3]
        MnD = month + day
        start_day = ''
        
        // int형인지 확인 작업
        int(MnD)
        
        if len(dot_split_str) == 3:
            start_day = find_start_day(dot_split_str[0],dot_split_str[1])
        return [month,day,MnD,start_day]
    except:
        return [0,0,0,0]

def find_start_day(mon, day):
    month = mon[-2:]
    days = day[1:3]
    MnD = month + days
    return MnD

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
    
    # link 추출 / 2월과 3월이 다름
    if len(event_body) == 3:
        link = event_title.select("a")[0].attrs['href']
    elif len(event_body) == 4:
        link = event_body[3].select("a")[0].attrs['href']
    else:
        link = "."
        
    date = event_body[2].text
    host = event_body[1].text
    date_info = find_due_day(event_body[2])
    due = date_info[2]
    start = date_info[3]
    
    return [event_title.text, link, date, host, due, start]
    

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
            date_range = today + 100
            if event_arr[5] == '':
                date_lim = int(event_arr[4])
            else:
                date_lim = int(event_arr[5])
                
            if (today <= int(event_arr[4])) and (date_range >= date_lim):
                content = f"[{event_arr[0]}]({event_arr[1]})" + "\n -" + event_arr[2] + "\n -"+ event_arr[3] + " <br/>\n "
                current_content += content
                
    return current_content
                
def __main__():
    url = 'https://github.com/brave-people/Dev-Event'
    date_now = 217 # 지금 날짜 int형으로
    html = get_html(url)
    event = split_event_html(html)

    
    script_title = '![](https://github.com/brave-people/Dev-Event/blob/master/static/title.PNG?raw=true)'
    
    print(content_list(script_title, event, date_now))

if __name__ == '__main__':
    __main__()
