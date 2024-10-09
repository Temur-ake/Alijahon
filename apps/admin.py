from django.contrib.admin import ModelAdmin, register

from apps.models import Category, Product, Region, District, Concurs, Order, Stream, User, SiteDeliveryPrices, \
    Transaction


# Register your models here.
@register(Product)
class ProductModelAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass


@register(Region)
class RegionModelAdmin(ModelAdmin):
    pass


@register(Concurs)
class ConcursModelAdmin(ModelAdmin):
    pass


@register(Order)
class ConcursModelAdmin(ModelAdmin):
    pass


@register(District)
class DistrictModelAdmin(ModelAdmin):
    list_display = ['name', ]


@register(Stream)
class StreamModelAdmin(ModelAdmin):
    pass


@register(User)
class UserModelAdmin(ModelAdmin):
    pass


@register(SiteDeliveryPrices)
class SiteDeliveryPricesModelAdmin(ModelAdmin):
    pass


@register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    pass
