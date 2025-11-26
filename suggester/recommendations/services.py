from django.core.cache import cache
from products.models import Product
from interactions.models import UserInteraction
from django.db.models import Count, Q
import random

class RecommendationEngine:
    """Базовый движок рекомендаций (заглушка для тестирования API)"""
    
    def get_content_based_recommendations(self, product_id, limit=10, stage_filter=None):
        """Content-based рекомендации"""
        try:
            target_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []

        base_query = Product.objects.exclude(id=product_id)
        
        if stage_filter:
            base_query = base_query.filter(stage=stage_filter)

        recommendations = base_query.filter(
            category=target_product.category
        )[:limit]

        if len(recommendations) < limit:
            additional = base_query.exclude(
                id__in=[r.id for r in recommendations]
            ).order_by('?')[:limit - len(recommendations)]
            recommendations = list(recommendations) + list(additional)
        
        return recommendations
    
    def get_collaborative_recommendations(self, product_id, limit=10):
        """Collaborative filtering (заглушка)"""
        return Product.objects.order_by('?')[:limit]
    
    def get_popular_recommendations(self, stage=None, limit=10):
        """Популярные товары"""
        base_query = Product.objects.all()
        if stage:
            base_query = base_query.filter(stage=stage)

        popular_products = base_query.annotate(
            positive_interactions=Count(
                'userinteraction',
                filter=Q(
                    userinteraction__interaction_type__in=['thumbs_up', 'add_to_cart', 'purchase']
                )
            )
        ).order_by('-positive_interactions', '-id')[:limit]
        
        return popular_products
    
    def get_hybrid_recommendations(self, product_id, session_id=None, limit=10, stage_filter=None):
        """Гибридные рекомендации"""
        return self.get_content_based_recommendations(product_id, limit, stage_filter)