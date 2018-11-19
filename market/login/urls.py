from django.conf.urls import url

from login.views import login, zc, forget, member, address, addAddress, location

urlpatterns =[
    url(r'^$', login, name="登录界面"),
    url(r'^zc/$', zc, name="注册界面"),
    url(r'^forget/$', forget, name="忘记密码界面"),
    url(r'^member/$', member, name="个人中心界面"),
    url(r'^address/$', address, name="收货地址界面"),
    url(r'^addAddress/$', addAddress, name="添加地址界面"),
    url(r'^location/$', location, name="定位界面"),
]