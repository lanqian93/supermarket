from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views import View

#商城首页
from goods.models import Cycle, Activity, SpecialGoods, Special, GoodsSku, Category


class IndexView(View):
    def get(self, request):
        cycles = Cycle.objects.filter(isDelete=False).order_by("order")
        acts = Activity.objects.all()
        specials = Special.objects.filter(is_on=True, isDelete=False).order_by("order")
        # sgs = SpecialGoods.objects.filter(special_id__name="特色专区")
        # print(sgs)
        # for sg in sgs:
        #     print(sg.sku_id.price)
        context = {
            "cycles": cycles,
            "acts": acts,
            # "sgs": sgs,
            "specials": specials,
        }
        return render(request, "goods/index.html", context)

    def post(self, request):
        pass


#商品详情页
class DetailView(View):
    def get(self, request, id):
        try:
            goods =GoodsSku.objects.get(pk=id, is_sale=True, isDelete=False)
        except GoodsSku.DoesNotExist:
            return redirect("goods:商品首页")
        context = {
            "goods": goods
        }
        return render(request, "goods/detail.html", context)
    def post(self):
        pass



#商品分类
class CategoryView(View):
    def get(self, request, cate_id, order):
        """
            综合,销量,价格,新品 排序规则需要程序员自己去定义参数,并且规定参数的含义

            0 综合
            1 销量
            2 价格降
            3 价格升
            4 新品

            定义一个列表:["id","-sales","-price","price","-add_time"]
        """
        #所有分类
        cs = Category.objects.filter(isDelete=False).order_by("order")
        #类型转换
        try:
            cate_id = int(cate_id)
            order = int(order)
        except:
            return redirect("goods:商品首页")
        if cate_id == 0:
            cate_id = cs.first().pk
        goods = GoodsSku.objects.filter(is_sale=True, isDelete=False, category_id=cate_id)
        #排序
        # if order == 0:  #综合排序
        #     goods = goods
        # if order == 1:  #销量排序
        #     goods = goods.order_by("sales")
        # if order == 2:   #价格降序
        #     goods = goods.order_by("-price")
        # if order == 3:    #价格升序
        #     goods = goods.order_by("price")
        # if order == 4:  #添加时间
        #     goods = goods.order_by("-add_time")
        order_rule = ["id", "-sales", "-price", "price", "-add_time"]
        try:
            order_one = order_rule[order]
        except:
            order_one = order_rule[0]
            order = 0
        goods = goods.order_by(order_one)
        #分页
        pageSize = 10
        pagniator = Paginator(goods, pageSize)
        #获取某页数据
        p = request.GET.get("p", 1)
        try:
            page = pagniator.page(p)
        except EmptyPage:
            page = pagniator.page(pagniator.num_pages)
        except PageNotAnInteger:
            page = pagniator.page(1)
        context = {
            "cs": cs,
            "goods": page,
            "cate_id": cate_id,
            "order": order,
        }
        return render(request, "goods/category.html", context)
    def post(self):
        pass