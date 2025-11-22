"""Админка для товаров."""

from django.contrib import admin
from .models import Product, ProductRelationship


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "stage", "price", "created_at"]
    list_filter = ["stage", "category", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["name", "description", "category", "stage"]}),
        ("Цена", {"fields": ["price"], "classes": ["collapse"]}),
        ("Атрибуты", {"fields": ["attributes"], "classes": ["collapse"]}),
        ("Даты", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]


@admin.register(ProductRelationship)
class ProductRelationshipAdmin(admin.ModelAdmin):
    list_display = ["source_product", "target_product", "relationship_type", "strength"]
    list_filter = ["relationship_type"]
    search_fields = ["source_product__name", "target_product__name"]
