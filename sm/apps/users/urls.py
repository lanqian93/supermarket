from django.conf.urls import url

from users.views import RegistView, LoginView, ForgetView, MemberView, UserInforView

urlpatterns = [
    url(r'^register/$', RegistView.as_view(), name='注册'),
    url(r'^login/$', LoginView.as_view(), name='登录'),
    url(r'^forget/$', ForgetView.as_view(), name='忘记密码'),
    url(r'^member/$', MemberView.as_view(), name='用户中心'),
    url(r'^information/$', UserInforView.as_view(), name='用户信息'),
]