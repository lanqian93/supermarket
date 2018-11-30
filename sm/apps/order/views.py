from _datetime import datetime
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from db.base_view import BaseVerifyView
from goods.models import GoodsSku
from django_redis import get_redis_connection

from order.models import Transport, Order, OrderGoods
from users.models import UserAddress

"""确认订单"""
class Tureorder(View):
    def get(self, request):
        #获取用户id
        user_id = request.session.get("id")
        if user_id is None:
            return redirect("user:登录")
        #处理收货地址，默认显示默认，没有，显示第一个
        address = UserAddress.objects.filter(isDelete=False, user_id=user_id).order_by("-isDeafault").first()
        #获取商品id
        sku_ids = request.GET.getlist("sku_id")
        if len(sku_ids) == 0:
            return redirect("cart:购物车页面")
        #准备键,获取商品数量
        r = get_redis_connection("default")
        cart_key = "cart_key_{}".format(user_id)
        #计算总价
        total = 0
        #获取完整商品信息
        goods = []
        for sku_id in sku_ids:
            try:
                sku_id = int(sku_id)
            except:
                return redirect("cart:购物车页面")
            #获取商品信息
            g = GoodsSku.objects.get(pk=sku_id)
            #获取商品数量
            count = r.hget(cart_key, sku_id)
            g.count = int(count)
            #计算总价
            total += int(count)*g.price
            goods.append(g)
        #运输方式
        transports = Transport.objects.filter(isDelete=False).order_by("price")
        context = {
            "goods": goods,
            "total": total,
            "address": address,
            "transports": transports,
        }
        return render(request, "order/tureorder.html", context)

    def post(self, request):
        # 下单的时候 一定要仔细, 判断都得加上
        # 判断用户是否登录
        user_id = request.session.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登录"})
        # 接收参数
        address_id = request.POST.get("address_id")
        sku_ids = request.POST.getlist("sku_id")
        transport_id = request.POST.get("transport")
        # 判断参数的合法性
        if not all([address_id, sku_ids, transport_id]):
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        try:
            address_id = int(address_id)
            transport_id = int(transport_id)
            skus = [int(sku_id) for sku_id in sku_ids]
        except:
            return JsonResponse({"code": 3, "errmsg": "参数错误"})
        # 判断收货地址和运输方式必须存在
        try:
            tran = Transport.objects.get(isDelete=False, pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "运输方式不存在"})
        try:
            address = UserAddress.objects.get(isDelete=False, pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse({"code": 5, "errmsg": "地址不存在"})
        #准备一个商品编号
        sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randint(10000, 99999))
        #准备地址
        ad = address.hcity + address.hproper + address.harea + address.street
        # 返回的订单基本信息对象
        order = Order.objects.create(sn=sn, user_id=user_id, username=address.username, phone=address.phone,
                             address=ad, transport=tran.transport_name, transport_price=tran.price)
        # 连接redis
        r = get_redis_connection("default")
        #准备key
        cart_key = "cart_key_{}".format(user_id)
        #先保存订单商品表
        # 准备个变量保存商品总价格
        total = 0
        for s in skus:
            # 保证商品也得存在
            try:
                goods = GoodsSku.objects.get(isDelete=False, is_sale=True, pk=s)
            except GoodsSku.DoesNotExist:
                return JsonResponse({"code": 6, "errmsg": "商品不存在"})
            # 获取购物车中的数量
            count = r.hget(cart_key, s)
            count = int(count)
            # 保证库存足够
            if count > goods.stock:
                return JsonResponse({"code": 7, "errmsg": "库存不足"})
            # 保存订单商品表
            OrderGoods.objects.create(order=order, goodsSku=goods, count=count, price=goods.price)
            # 销库存加
            goods.stock -= count
            #销量增加
            goods.sales += count
            # 保存
            goods.save()
            # 统计总价格
            total += goods.price*count
        # 计算订单的总金额
        order.order_price = total + tran.price
        try:
            order.save()
        except:
            return JsonResponse({"code": 8, "errmsg": "保存商品总金额失败"})
        # 所有都成功, 删除购物车中的数据
        #r.hdel(cart_key, *skus)
        return JsonResponse({"code": 0, "msg": "生成订单成功", "sn": sn})


"""确认支付"""
class Pay(BaseVerifyView):
    def get(self, request):
        #接受参数
        sn = request.GET.get("sn")
        user_id = request.session.get("id")
        #查询订单
        try:
            order = Order.objects.get(sn=sn, user_id=user_id, isDelete=False)
        except Order.DoesNotExist:
            return redirect("cart:购物车页面")
        tol = order.order_price - order.transport_price
        context = {
            "order": order,
            "tol": tol
        }
        return render(request, "order/order.html", context)
    def post(self, request):
        pass