from django.conf.urls import url

from goods.views import IndexView, DetailView, CategoryView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="商品首页"),
    url(r'^(?P<id>\d+).html$', DetailView.as_view(), name="商品详情"),
    url(r'^category/(?P<cate_id>\d+)/(?P<order>\d+)$', CategoryView.as_view(), name="商品分类"),
]