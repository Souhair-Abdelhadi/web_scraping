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



def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request,'articles/article_list.html',{'articles' : articles})

def item(request):
    return render(request,'articles/item.html')

def article_details(request,slug):
    return HttpResponse(slug)

def jumia_item(request):

    list = []
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'fr-FR, fr;q=0.5'})

    try:
        print(request.GET.get('q',''))
        html = requests.get("https://www.jumia.ma/catalog/?q={}".format(request.GET.get('q','')),headers=HEADERS)
        bs = BeautifulSoup(html.text,'lxml')
        nameList = bs.find_all('article',{'class' : 'c-prd'})
        #nameList = bs.select("span.a-price-whole")
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('the server could not be found!')
    except AttributeError as e:
        print("tag was not found") 
    else:
        if nameList == None:
            print("tag was not found")
        for i in nameList:
            description = i.find('h3',{'class' : 'name'})
            price = i.find('div',{'class' : 'prc'})
            rate = i.find('div',{'class' : 'stars'})
            # image = i.find('img',{'class' : 's-image'})
            global v_price,v_rate,v_description
            v_price = ''
            v_rate = ''
            v_description = ''
            if price is not None:
                v_price = price.get_text()
                if description is not None:
                    v_description = description.get_text()
                if rate is not None:
                    v_rate = rate.get_text()
            list.append(json.dumps({'price':v_price,'description':v_description.replace('"',''),'rate':v_rate}))
        #print(list)

    a_list = set()
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'fr-Fr, fr;q=0.5'})

    try:
        html = requests.get("https://www.amazon.fr/s?k={}&page={}".format(request.GET.get('q',''),1),headers=HEADERS)
        bs = BeautifulSoup(html.text,'lxml')
        nameList = bs.find_all('div',{'class' : 'sg-col-inner'})
        #nameList = bs.select("span.a-price-whole")
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('the server could not be found!')
    except AttributeError as e:
        print("tag was not found") 
    else:
        if nameList == None:
            print("tag was not found")
        for i in nameList:
            title = i.find('span',{'class' : 'a-size-base-plus'})
            description = i.find('span',{'class' : 'a-text-normal'})
            price = i.find('span',{'class' : 'a-price-whole'})
            rate = i.find('span',{'class' : 'a-icon-alt'})
            # image = i.find('img',{'class' : 's-image'})
            global a_price,a_rate,a_title,a_description
            a_price = ''
            a_title = ''
            a_rate = ''
            a_description = ''
            if price is not None :
                a_price = price.get_text()
                if title is not None:
                    a_title = title.get_text()
                if description is not None:
                    a_description = description.get_text()
                if rate is not None:
                    a_rate = rate.get_text()
                a_list.add(json.dumps({'price':a_price,'title':a_title,'description':re.sub('"','',a_description),'rate':a_rate}))
                print(a_list)
                
    return render(request,'articles/jumia_item.html',{'items':list,'amazonItems':a_list})