from django.conf.urls import url

from order.views import Tureorder, Pay

urlpatterns = [
    url(r"^tureorder", Tureorder.as_view(), name="确认订单"),
    url(r"^pay", Pay.as_view(), name="确认支付"),
]