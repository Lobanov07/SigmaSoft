from django.db import models
from products.models import Product

class UserSession(models.Model):
    session_id = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="ID сессии"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.session_id


class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'Просмотр'),
        ('thumbs_up', 'Лайк'),
        ('thumbs_down', 'Дизлайк'),
        ('add_to_cart', 'Добавление в корзину'),
        ('purchase', 'Покупка'),
    ]
    
    session = models.ForeignKey(
        UserSession, 
        on_delete=models.CASCADE, 
        related_name='interactions',
        verbose_name="Сессия"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    interaction_type = models.CharField(
        max_length=20, 
        choices=INTERACTION_TYPES,
        verbose_name="Тип взаимодействия"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время")
    metadata = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name="Метаданные"
    )
    
    class Meta:
        verbose_name = "Взаимодействие"
        verbose_name_plural = "Взаимодействия"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['session', 'timestamp']),
            models.Index(fields=['product', 'interaction_type']),
        ]
    
    def __str__(self):
        return f"{self.session} - {self.product} - {self.get_interaction_type_display()}"