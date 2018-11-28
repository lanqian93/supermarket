from django.db import models



# """支付方式"""
# class Payment(models.Model):
#     pay_name = models.CharField(max_length=50, verbose_name="支付方式")
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
#     isDelete = models.BooleanField(default=False, verbose_name="是否删除")
#     class Meta:
#         verbose_name = "支付管理"
#         verbose_name_plural = verbose_name
#     def __str__(self):
#         return self.pay_name
#
#
# """运输方式"""
# class Transport(models.Model):
#     transport_name = models.CharField(max_length=50, verbose_name="运输方式")
#     price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="运输费用")
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
#     isDelete = models.BooleanField(default=False, verbose_name="是否删除")
#     class Meta:
#         verbose_name = "运输方式管理"
#         verbose_name_plural = verbose_name
#     def __str__(self):
#         return self.transport_name