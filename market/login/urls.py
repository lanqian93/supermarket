from django.conf.urls import url

from login.views import login, zc, forget

urlpatterns =[
    url(r'^$', login, name="登录界面"),
    url(r'^zc/$', zc, name="注册界面"),
    url(r'^forget/$', forget, name="忘记密码界面"),
]