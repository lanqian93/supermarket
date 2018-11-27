from django.conf.urls import url

from cart.views import AddCartView, ShopCartView

urlpatterns = [
    url(r'^$',  AddCartView.as_view(), name="添加购物车"),
    url(r'^shopcart$',  ShopCartView.as_view(), name="购物车页面"),
]