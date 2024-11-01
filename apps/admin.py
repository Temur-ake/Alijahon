from django.contrib.admin import ModelAdmin, register
from django.utils.safestring import mark_safe

from apps.models import Category, Product, Region, District, Concurs, Order, Stream, User, SiteDeliveryPrices, \
    Transaction


# Register your models here.
@register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'display_image', 'payment_referral']
    search_fields = ['name', 'description']
    readonly_fields = ["display_image"]

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="70" height="60" />'.format(
                url=obj.image.url,
            ))
        return "No image"

    display_image.short_description = 'Image'


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = ['name', 'display_image']
    readonly_fields = ["display_image"]

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="70" height="60" />'.format(
                url=obj.image.url,
            ))
        return "No image"

    display_image.short_description = 'Image'


@register(Region)
class RegionModelAdmin(ModelAdmin):
    pass


@register(Concurs)
class ConcursModelAdmin(ModelAdmin):
    list_display = ['name', 'display_image', 'start_date', 'end_date']

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="70" height="60" />'.format(
                url=obj.image.url,
            ))
        return "No image"

    display_image.short_description = 'Image'


@register(Order)
class ConcursModelAdmin(ModelAdmin):
    list_display = 'product', 'quantity', 'full_name', 'stream', 'status', 'courier'
    search_fields = (
        'product__name',
        'full_name',
        'status',
        'stream__name',
        'courier__phone',
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


@register(District)
class DistrictModelAdmin(ModelAdmin):
    list_display = ['name', 'region']


@register(Stream)
class StreamModelAdmin(ModelAdmin):
    list_display = 'name', 'product', 'discount', 'owner'
    search_fields = (
        'product__name',
        'discount',
        'owner__phone',
        'name'
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


@register(User)
class UserModelAdmin(ModelAdmin):
    list_display = ['phone', 'first_name', 'last_name', 'type', 'balance', 'display_image', 'address', 'district']
    search_fields = (
        'first_name',
        'last_name',
        'phone',
        'type'
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="70" height="60" />'.format(
                url=obj.image.url,
            ))
        return "No image"

    display_image.short_description = 'Image'


@register(SiteDeliveryPrices)
class SiteDeliveryPricesModelAdmin(ModelAdmin):
    list_display = 'price_for_all_regions', 'price_for_tashkent_region', 'price_for_inside_of_tashkent'


@register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    list_display = 'owner', 'status', 'amount', 'display_image', 'owner__type', 'card_number'
    search_fields = (
        'owner__phone',
        'card_number',
        'status'
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="70" height="60" />'.format(
                url=obj.image.url,
            ))
        return "No image"

    display_image.short_description = 'Image'
