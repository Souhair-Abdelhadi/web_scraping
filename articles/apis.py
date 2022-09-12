from dataclasses import replace
from decimal import DivisionByZero
from django.views import View
from django.http import JsonResponse
import json
from asyncio.windows_events import NULL
from cgitb import text
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.error import URLError
from bs4 import BeautifulSoup
from requests import request
import requests
import re


class Jumia(View):
    def get(self,request):
        list = []
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'fr-FR, fr;q=0.5','Access-Control-Allow-Origin': '*'})
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
            v_price = ''
            v_rate = ''
            v_description = ''
            v_img = ''
            moy = 0
            for i in nameList:
                description = i.find('h3',{'class' : 'name'})
                price = i.find('div',{'class' : 'prc'})
                rate = i.find('div',{'class' : 'stars'})
                img = i.find('img',{'class' : 'img'})
                if price is not None  and len(price.get_text()) > 0 :
                    v_price = price.get_text()
                    try:
                        l_price = v_price.split("-")
                        moy += float(re.sub(',','',l_price[0].replace("Dhs","").replace(" ","").rstrip()))
                    except ValueError:
                        print('error at jumia api')
                    if description is not None:
                        v_description = description.get_text()
                    if rate is not None:
                        v_rate = rate.get_text()
                    if img is not None:
                        v_img = img['data-src']
                list.append(json.dumps({'price':v_price,'description':v_description.replace('"',''),'rate':v_rate,'image':v_img}))
            res = {
                'list' : list,
                'moy' : moy / len(list) if len(list) > 0 else 0
            }
            return JsonResponse(res)


class Amazon(View):
    def get(slef,request):
        a_list = []
        moy = 0
        item = request.GET.get('q','')
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'fr-Fr, fr;q=0.5'})
        for page in range(1,5):
            try:
                html = requests.get("https://www.amazon.fr/s?k={}&page={}".format(item,page),headers=HEADERS)
                bs = BeautifulSoup(html.text,'lxml')
                nameList = bs.find_all('div',{'class' : 'sg-col-inner'})
                #nameList = bs.select("span.a-price-whole")
            except HTTPError as e:
                print(e)
            except URLError as e:
                print('the server could not be found!')
            except AttributeError as e:
                print("tag was not found") 
            except ConnectionError as  e:
                print('coonection error')
            else:
                if nameList == None:
                    print("tag was not found")
                a_price = ''
                a_title = ''
                a_rate = ''
                a_description = ''
                a_img = ''
                for i in nameList:
                    title = i.find('span',{'class' : 'a-size-base-plus'})
                    description = i.find('span',{'class' : 'a-text-normal'})
                    price = i.find('span',{'class' : 'a-price-whole'})
                    rate = i.find('span',{'class' : 'a-icon-alt'})
                    img = i.find('img',{'class' : 's-image'})
                    # image = i.find('img',{'class' : 's-image'})
                    if price is not None and len(price.get_text()) > 0:
                        a_price = price.get_text()
                        try:
                            l_price = a_price.split("-")
                            v_l_price = l_price[0].replace(' ','')
                            v_l_price = re.sub(',','.',v_l_price.rstrip())      
                            moy += float(v_l_price) * 9.7
                        except ValueError:
                            print('value error at amazon api ',v_l_price)
                        if title is not None:
                            a_title = title.get_text()
                        if description is not None:
                            a_description = description.get_text()
                        if rate is not None:
                            a_rate = rate.get_text()
                        if img is not None:
                            a_img = img['src']
                        # if title.get_text().find(item) != -1:
                        #     print("amazon api test executed")
                        a_list.append(json.dumps({'price':a_price,'title':a_title,'description':re.sub('"','',a_description),'rate':a_rate
                            ,'image':a_img}))
                        if len(a_list) > 20:
                            break
        res = {
            'list': a_list,
            'moy' : moy / len(a_list) if len(a_list) > 0 else 1
        }

        return JsonResponse(res)


