from django.db import models


"""运输方式"""
class Transport(models.Model):
    transport_name = models.CharField(max_length=50, verbose_name="运输方式")
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="运输费用")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "运输方式管理"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.transport_name


"""支付方式"""
class Payment(models.Model):
    pay_name = models.CharField(max_length=50, verbose_name="支付方式")
    img = models.ImageField(upload_to="pay/%Y", verbose_name="图片")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "支付管理"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.pay_name

"""订单基本信息表"""
class Order(models.Model):
    order_status = (
        (0, "待付款"), (1, "已付款"), (2, "待发货"), (3, "已发货"), (4, "待评价"), (5, "申请退款"),
        (6, "已退款"), (7, "完成"), (8, "取消订单")
    )
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    sn = models.CharField(max_length=100, verbose_name="订单编号", unique=True)
    order_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单金额", default=0)
    user = models.ForeignKey(to="users.Users", verbose_name="用户id")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11, verbose_name="收货人电话")
    address = models.CharField(max_length=255, verbose_name="收货人地址")
    status = models.SmallIntegerField(choices=order_status, default=0, verbose_name="订单状态")
    transport = models.CharField(max_length=50, verbose_name="运输方式")
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="运费")
    payment = models.ForeignKey(to="Payment", verbose_name="付款方式", null=True, blank=True)
    real_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="实付金额", default=0)
    def __str__(self):
        return self.sn
    class Meta:
        verbose_name = "订单基本信息管理"
        verbose_name_plural = verbose_name


"""订单商品表"""
class OrderGoods(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    order = models.ForeignKey(to="Order", verbose_name="订单id")
    goodsSku = models.ForeignKey(to="goods.GoodsSku", verbose_name="sku_id")
    count = models.IntegerField(verbose_name="订单商品数量")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单商品价格")
    def __str__(self):
        return self.order.sn
    class Meta:
        verbose_name = "订单商品管理"
        verbose_name_plural = verbose_name