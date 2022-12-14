"""web_scrapping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path as url,include,path
from django.contrib import admin
from . import views
from django.views.static import serve
from django.conf import settings



static_urlpatterns = [
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$',views.homepage),
    # url(r'^about/',views.about),
    url(r'^',include('articles.urls')),
    path("",include(static_urlpatterns))
]
 

handler404 = "web_scrapping.views.pageNotFound"