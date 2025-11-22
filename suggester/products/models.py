"""Модели, связанные с товарами."""

from django.db import models


class Product(models.Model):
    STAGE_CHOICES = [
        ("white_box", "White Box"),
        ("finishing", "Finishing"),
        ("furniture", "Furniture"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.CharField(max_length=100, verbose_name="Категория")
    stage = models.CharField(
        max_length=50,
        choices=STAGE_CHOICES,
        default="white_box",
        verbose_name="Этап ремонта",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена"
    )
    attributes = models.JSONField(default=dict, blank=True, verbose_name="Атрибуты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_stage_display()})"


class ProductRelationship(models.Model):
    RELATIONSHIP_TYPES = [
        ("complementary", "Дополняющий"),
        ("alternative", "Альтернативный"),
        ("frequently_bought", "Часто покупают вместе"),
    ]

    source_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="source_relationships",
        verbose_name="Исходный товар",
    )
    target_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="target_relationships",
        verbose_name="Целевой товар",
    )
    relationship_type = models.CharField(
        max_length=50, choices=RELATIONSHIP_TYPES, verbose_name="Тип связи"
    )
    strength = models.FloatField(default=1.0, verbose_name="Сила связи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Связь товаров"
        verbose_name_plural = "Связи товаров"
        unique_together = ["source_product", "target_product", "relationship_type"]

    def __str__(self):
        return f"{self.source_product} -> {self.target_product} ({self.get_relationship_type_display()})"
