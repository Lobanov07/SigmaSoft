from rest_framework import serializers
from products.models import Product, ProductRelationship
from interactions.models import UserSession, UserInteraction

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров."""
    
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'category', 
            'stage',
            'stage_display',
            'price', 
            'attributes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductRelationshipSerializer(serializers.ModelSerializer):
    """Сериализатор для связей товаров."""

    source_product = ProductSerializer(read_only=True)
    target_product = ProductSerializer(read_only=True)
    relationship_type_display = serializers.CharField(
        source='get_relationship_type_display', 
        read_only=True
    )
    
    class Meta:
        model = ProductRelationship
        fields = [
            'id',
            'source_product',
            'target_product', 
            'relationship_type',
            'relationship_type_display',
            'strength',
            'created_at'
        ]


class UserInteractionSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействий пользователей."""

    product = ProductSerializer(read_only=True)
    interaction_type_display = serializers.CharField(
        source='get_interaction_type_display', 
        read_only=True
    )
    
    class Meta:
        model = UserInteraction
        fields = [
            'id',
            'session',
            'product',
            'interaction_type',
            'interaction_type_display',
            'timestamp',
            'metadata'
        ]
        read_only_fields = ['timestamp']


class RecommendationSerializer(serializers.Serializer):
    """Сериализатор для рекомендаций."""
    product = ProductSerializer()
    score = serializers.FloatField(required=False, allow_null=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    algorithm = serializers.CharField(required=False, allow_blank=True)


class FeedbackSerializer(serializers.Serializer):
    """Сериализатор для получения фидбека."""

    session_id = serializers.CharField(max_length=100, required=True)
    product_id = serializers.IntegerField(required=True)
    feedback = serializers.ChoiceField(
        choices=['thumbs_up', 'thumbs_down'],
        required=True
    )
    source = serializers.CharField(
        max_length=50, 
        required=False, 
        default='unknown'
    )
    algorithm_version = serializers.CharField(
        max_length=50, 
        required=False, 
        default='1.0'
    )


class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для сессий."""

    class Meta:
        model = UserSession
        fields = ['session_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка товаров."""

    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'stage', 'stage_display', 'price']