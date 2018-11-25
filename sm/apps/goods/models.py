from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from sm import settings

"""商品分类表"""
class Category(models.Model):
    cate_name = models.CharField(max_length=50, verbose_name="分类名")
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="分类简介")
    order = models.SmallIntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.cate_name

"""商品Spu表"""
class GoodsSpu(models.Model):
    spu_name = models.CharField(max_length=50, verbose_name="名称")
    detail = RichTextUploadingField(verbose_name="详情")
    class Meta:
        verbose_name = "商品spu"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.spu_name


"""商品sku表"""
class GoodsSku(models.Model):
    unit_choices = (
        (1, "箱"),
        (2, "斤"),
        (3, "个"),
    )   #单独用个单位表好取值一点
    spu_id = models.ForeignKey(to="GoodsSpu", verbose_name="商品spu")
    sku_name = models.CharField(max_length=50, verbose_name="商品名")
    desc = models.CharField(max_length=100, verbose_name="简介", null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="价格")
    unit = models.SmallIntegerField(choices=unit_choices, default=3, verbose_name="单位")
    stock = models.IntegerField(default=0, verbose_name="库存")
    sales = models.IntegerField(default=0, verbose_name="销量")
    url = models.ImageField(verbose_name='封面图片', upload_to='goods/%Y%m/%d')
    is_sale = models.BooleanField(default=True, verbose_name="是否上架")
    category_id = models.ForeignKey(to="Category", verbose_name="商品分类id")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    def show_url(self):
        return "<img style='width:80px' src='{}{}'/>".format(settings.MEDIA_URL, self.url)
    show_url.allow_tags = True
    show_url.short_description = "url"

    class Meta:
        verbose_name = "商品sku"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.sku_name


"""商品相册"""
class GoodsImg(models.Model):
    url = models.ImageField(verbose_name='商品相册', upload_to='goods_gallery/%Y%m/%d')
    sku_id = models.ForeignKey(to="GoodsSku", verbose_name="商品sku id")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "商品相册"
        verbose_name_plural = verbose_name



"""首页轮播商品"""
class Cycle(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称")
    sku_id = models.ForeignKey(to=GoodsSku, verbose_name="商品sku id")
    url = models.ImageField(verbose_name="图片地址", upload_to='banner/%Y%m/%d')
    order = models.SmallIntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "轮播商品"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


"""首页活动表"""
class Activity(models.Model):
    name = models.CharField(max_length=50, verbose_name="活动名")
    url = models.ImageField(verbose_name="活动图片地址", upload_to='activity/%Y%m/%d')
    a_url = models.URLField(verbose_name="活动url地址", max_length=200)
    class Meta:
        verbose_name = "活动"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


"""首页活动专区"""
class Special(models.Model):
    name = models.CharField(max_length=50, verbose_name="活动专区名称")
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="描述")
    order = models.SmallIntegerField(default=0, verbose_name="排序")
    is_on = models.BooleanField(default=True, verbose_name="是否上架")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "活动专区"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

"""首页专区活动商品表"""
class SpecialGoods(models.Model):
    special_id = models.ForeignKey(to="Special", verbose_name="活动专区id")
    sku_id = models.ForeignKey(to="GoodsSku", verbose_name="商品sku id")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "活动商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku_id.sku_name


