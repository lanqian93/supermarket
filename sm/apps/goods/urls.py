from django.conf.urls import url

from goods.views import IndexView, DetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="商品首页"),
    url(r'^detail/$', DetailView.as_view(), name="商品详情"),
]