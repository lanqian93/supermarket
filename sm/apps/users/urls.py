from django.conf.urls import url

from users.views import RegistView, LoginView, ForgetView, MemberView, UserInforView, AddressListView, AddAddressView, \
    send_code, AddressEditView, AdressDelView, defaultAddress

urlpatterns = [
    url(r'^register/$', RegistView.as_view(), name='注册'),
    url(r'^login/$', LoginView.as_view(), name='登录'),
    url(r'^forget/$', ForgetView.as_view(), name='忘记密码'),
    url(r'^member/$', MemberView.as_view(), name='用户中心'),
    url(r'^information/$', UserInforView.as_view(), name='用户信息'),
    url(r'^addresses/$', AddressListView.as_view(), name='收货地址列表'),
    url(r'^addaddress/$', AddAddressView.as_view(), name='添加地址'),
    url(r'^editaddress/(?P<id>\d+)$', AddressEditView.as_view(), name='修改地址'),
    url(r'^deladdress', AdressDelView.as_view(), name='删除地址'),
    url(r'^defaultaddress', defaultAddress, name='设置默认地址'),
    url(r'^sendcode/$', send_code, name='发送验证码'),
]