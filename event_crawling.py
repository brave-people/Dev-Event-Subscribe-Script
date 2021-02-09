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