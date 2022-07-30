from django.urls import re_path as url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .apis import Articles,Amazon

urlpatterns = [
    # url(r'^$',views.article_list),
    # url(r'^jumia/$',views.jumia_item),
    url(r'^$',views.item),
    url(r'^jumia_api/$',Articles.as_view()),
    url(r'^amazon_api/$',Amazon.as_view()),
    # url(r'^(?P<slug>[\w-]+/$)',views.article_details),
   
]

urlpatterns += staticfiles_urlpatterns()