from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from goods.models import GoodsSku


class AddCartView(View):
    def get(self, request):
        """
               1. 需要验证登陆
               2. 接收参数: 购物车加入数量(count),当前商品ID(sku_id)
               3. 验证数据
                   a. 都必须为整数
                   b. count 必须大于0
                   c. 商品必须存在
                   d. (可以有) 判断库存

               4. 添加商品到购物车中(通过redis实现)
                   存好处存 , 取好取
                   user_id  sku_id count
                   hash 对象: object = {"key1":value1,"key2":value2}
                       HSET key field value
                       HSET cart_key_user_id sku_id count

               5. 填写成功,返回
                   返回是否成功, 及 购物车中总的商品的数量

           """
        pass
    def post(self, request):
        #1. 需要验证登陆
        user_id = request.session.get("id")
        if user_id is None:
            #没有登录
            return JsonResponse({"code": 1, "errmsg": "没有登录"})
        # 接收参数: 购物车加入数量(count), 当前商品ID(sku_id)
        count = request.POST.get("count")
        sku_id = request.POST.get("sku_id")
        # 验证数据
        # a.都必须为整数
        try:
            count = int(count)
            sku_id = int(sku_id)
        except:
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        # b.count 必须大于0
        # if count <= 0:
        #     return JsonResponse({"code": 3, "errmsg": "参数错误"})
        # c.商品必须存在
        try:
            goodssku = GoodsSku.objects.get(pk=sku_id)
        except GoodsSku.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "商品不存在"})
        # d.(可以有) 判断库存
        if count > goodssku.stock:
            return JsonResponse({"code": 5, "errmsg": "库存不足"})
        # 4.添加商品到购物车中(通过redis实现)
        r = get_redis_connection('default')
        cart_key = "cart_key_{}".format(user_id)
        res = r.hincrby(cart_key, sku_id, count)
        # 判断当前sku_id中的数量如果等于0说明 需要从redis中删除该sku_id对应的键
        if res == 0:
            r.hdel(cart_key, sku_id)
        # 获取购物车中总数量
        cart_count = 0
        vals = r.hvals(cart_key)
        for v in vals:
            cart_count += int(v)

        #成功返回
        return JsonResponse({"code": 0, "cart_count": cart_count})



#购物车页面
class ShopCartView(BaseVerifyView):
    def get(self, request):
        # 获取商品sku
        user_id = request.session.get("id")
        r = get_redis_connection('default')
        cart_key = "cart_key_{}".format(user_id)
        datas = r.hgetall(cart_key)  #二进制字典
        goodsskus = []
        for sku_id, count in datas.items():
            sku_id = int(sku_id)
            count = int(count)
            # 查询商品的完整信息
            goods = GoodsSku.objects.get(pk=sku_id)
            # 将count保存到 商品对象上(对象上添加一个自定义的属性)
            goods.count = count
            # 保存到列表
            goodsskus.append(goods)
        context = {
            "goodsskus": goodsskus,
        }
        return render(request, "cart/shopcart.html", context)
    def post(self, request):
        pass