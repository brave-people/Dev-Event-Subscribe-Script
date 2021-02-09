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