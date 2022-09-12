from django.urls import re_path as url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .apis import Jumia,Amazon

urlpatterns = [
    url(r'^$',views.item),
    url(r'^jumia_api/$',Jumia.as_view()),
    url(r'^amazon_api/$',Amazon.as_view()),
   
]

urlpatterns += staticfiles_urlpatterns()