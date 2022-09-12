import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from asyncio.windows_events import NULL
from cgitb import text
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.error import URLError
from bs4 import BeautifulSoup
from requests import RequestException, request
import requests




def item(request):
    return render(request,'articles/item.html')
