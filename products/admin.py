from django.contrib import admin
from .models import PurchaseOrder, Product, StandardSizeChart

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'date', 'brand', 'article_type', 'origin_country', 'created_at']
    list_filter = ['brand', 'article_type', 'date']
    search_fields = ['po_number', 'brand']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'size', 'color', 'quantity']
    list_filter = ['size', 'color']
    search_fields = ['purchase_order__po_number', 'color']

@admin.register(StandardSizeChart)
class StandardSizeChartAdmin(admin.ModelAdmin):
    list_display = ['size', 'A_length_from_shoulder', 'B_chest_width', 'I_sleeve_length']
    list_filter = ['size']