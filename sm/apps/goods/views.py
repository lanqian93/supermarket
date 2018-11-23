from django.shortcuts import render
from django.views import View

#商城首页
class IndexView(View):
    def get(self, request):
        return render(request, "goods/index.html")

    def post(self, request):
        pass


#商品详情页
class DetailView(View):
    def get(self, request):
        return render(request, "goods/detail.html")
    def post(self):
        pass