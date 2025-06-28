from django.contrib import admin
from .models import Product, Order, OrderedItem,Review
from django.utils.html import format_html


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status', 'is_seen_by_admin', 'complete')
    list_filter = ('status', 'is_seen_by_admin', 'complete')
    search_fields = ('user__username', 'id')

    actions = ['mark_as_seen']

    def mark_as_seen(self, request, queryset):
        queryset.update(is_seen_by_admin=True)
        self.message_user(request, "Selected orders marked as seen.")

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','image_tag', 'name', 'category', 'price', 'created_at')  # adjust fields as per your model
    search_fields = ('name', 'category')  # example if you have category relation

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)
admin.site.register(Review)