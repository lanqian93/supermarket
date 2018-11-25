from django.contrib import admin

# Register your models here.
from goods.models import Category, GoodsSpu, GoodsSku, GoodsImg, Cycle, Activity, Special, SpecialGoods

# admin.site.register(Category)
# admin.site.register(GoodsSpu)
# admin.site.register(GoodsSku)
# admin.site.register(GoodsImg)
# admin.site.register(Cycle)
admin.site.register(Activity)
# admin.site.register(Special)
admin.site.register(SpecialGoods)


"""分类注册"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'cate_name', 'desc', 'order']
    list_filter = ['cate_name']
    list_display_links = ['id', 'cate_name']

    #spu管理
    class CategoryAdminInline(admin.TabularInline):
        model = GoodsSku
        extra = 1
    inlines = [CategoryAdminInline]

"""商品spu注册"""
@admin.register(GoodsSpu)
class GoodSpuAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'spu_name', 'detail']
    list_display_links = ['id', 'spu_name']
    list_filter = ['spu_name']

    #sku的管理
    class GoodSpuAdminInline(admin.TabularInline):
        model = GoodsSku
        extra = 1
    inlines = [GoodSpuAdminInline]


"""商品sku注册"""
@admin.register(GoodsSku)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'spu_id', 'sku_name', 'price', 'unit', 'stock', 'sales', 'show_url', 'is_sale', 'category_id']
    list_display_links = ['id', 'sku_name']
    class SpecialGoodsAdminInline(admin.TabularInline):
        model = SpecialGoods
        extra = 1

    class GoodsImgAdminInline(admin.TabularInline):
        model = GoodsImg
        extra = 1
    inlines = [SpecialGoodsAdminInline, GoodsImgAdminInline]


"""轮播注册"""
@admin.register( Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display_links = ['id', 'name']
    list_display = ['id', 'name', 'sku_id', 'url', 'order']


"""活动专区"""
@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_per_page = 10
    # list_display_links = ['id', 'name']
    exclude = ['add_time', 'update_time', 'isDelete']
    #活动专区商品管理
    class SpecialGoodsAdminInline(admin.TabularInline):
        model = SpecialGoods
        extra = 1
    inlines = [SpecialGoodsAdminInline]