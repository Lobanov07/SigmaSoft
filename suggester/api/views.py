from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.http import JsonResponse

from products.models import Product
from interactions.models import UserSession, UserInteraction
from recommendations.services import RecommendationEngine
from .serializers import *


class ProductListAPIView(APIView):
    """API для получения списка товаров"""

    def get(self, request):
        stage = request.GET.get("stage", "white_box")
        category = request.GET.get("category")
        limit = int(request.GET.get("limit", 20))

        products = Product.objects.filter(stage=stage)

        if category:
            products = products.filter(category=category)

        products = products.order_by("name")[:limit]

        serializer = ProductListSerializer(products, many=True)
        return Response(
            {"count": len(products), "stage": stage, "products": serializer.data}
        )


class ProductDetailAPIView(APIView):
    """API для получения детальной информации о товаре"""

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductRecommendationsAPIView(APIView):
    """API для получения рекомендаций к товару"""

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # параметры
        session_id = request.GET.get("session_id")
        limit = int(request.GET.get("limit", 6))
        stage_filter = request.GET.get("stage", "white_box")
        algorithm = request.GET.get("algorithm", "hybrid")

        #  движок рекомендаций
        engine = RecommendationEngine()

        #  рекомендации в зависимости от алгоритма
        if algorithm == "content":
            recommendations = engine.get_content_based_recommendations(
                product_id, limit, stage_filter
            )
        elif algorithm == "collaborative":
            recommendations = engine.get_collaborative_recommendations(
                product_id, limit
            )
        elif algorithm == "popular":
            recommendations = engine.get_popular_recommendations(stage_filter, limit)
        else:  # hybrid
            recommendations = engine.get_hybrid_recommendations(
                product_id, session_id, limit, stage_filter
            )

        #  просмотр в историю если есть сессия
        if session_id:
            try:
                session = UserSession.objects.get(session_id=session_id)
                UserInteraction.objects.create(
                    session=session,
                    product=product,
                    interaction_type="view",
                    metadata={"source": "recommendation_api", "algorithm": algorithm},
                )
            except UserSession.DoesNotExist:
                pass  # Сессия не найдена, пропускаем

        #  ответ с причинами рекомендаций
        recommendation_data = []
        for rec in recommendations:
            reason = self._get_recommendation_reason(product, rec, algorithm)
            recommendation_data.append(
                {"product": rec, "reason": reason, "algorithm": algorithm}
            )

        serializer = RecommendationSerializer(recommendation_data, many=True)

        return Response(
            {
                "main_product": ProductSerializer(product).data,
                "recommendations": serializer.data,
                "algorithm_used": algorithm,
                "count": len(recommendations),
            }
        )

    def _get_recommendation_reason(self, main_product, recommended_product, algorithm):
        """Определяет причину рекомендации"""
        if algorithm == "content":
            if main_product.category == recommended_product.category:
                return "Товар из той же категории"
            return "Похожий товар"
        elif algorithm == "collaborative":
            return "Часто покупают вместе"
        elif algorithm == "popular":
            return "Популярный товар"
        else:
            return "Персональная рекомендация"


class FeedbackAPIView(APIView):
    """API для отправки фидбека по рекомендациям"""

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data


            session, created = UserSession.objects.get_or_create(
                session_id=data["session_id"]
            )


            try:
                product = Product.objects.get(id=data["product_id"])
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            #  взаимодействие
            interaction = UserInteraction.objects.create(
                session=session,
                product=product,
                interaction_type=data["feedback"],
                metadata={
                    "source": data.get("source", "unknown"),
                    "algorithm_version": data.get("algorithm_version", "1.0"),
                },
            )

            return Response(
                {
                    "status": "success",
                    "interaction_id": interaction.id,
                    "message": "Feedback recorded successfully",
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSessionAPIView(APIView):
    """API для создания новой пользовательской сессии"""

    def post(self, request):
        session = UserSession.objects.create()
        serializer = SessionSerializer(session)
        return Response(serializer.data)


class UserInteractionsAPIView(APIView):
    """API для получения истории взаимодействий пользователя"""

    def get(self, request):
        session_id = request.GET.get("session_id")

        if not session_id:
            return Response(
                {"error": "session_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = UserSession.objects.get(session_id=session_id)
            interactions = UserInteraction.objects.filter(session=session).order_by(
                "-timestamp"
            )

            serializer = UserInteractionSerializer(interactions, many=True)

            return Response(
                {
                    "session_id": session_id,
                    "interactions_count": interactions.count(),
                    "interactions": serializer.data,
                }
            )

        except UserSession.DoesNotExist:
            return Response(
                {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PopularProductsAPIView(APIView):
    """API для получения популярных товаров"""

    def get(self, request):
        stage = request.GET.get("stage", "white_box")
        limit = int(request.GET.get("limit", 10))

        #  положительные взаимодействия (лайки, добавления в корзину, покупки)
        popular_products = (
            Product.objects.filter(stage=stage)
            .annotate(
                positive_interactions=Count(
                    "userinteraction",
                    filter=Q(
                        userinteraction__interaction_type__in=[
                            "thumbs_up",
                            "add_to_cart",
                            "purchase",
                        ]
                    ),
                )
            )
            .order_by("-positive_interactions", "-id")[:limit]
        )

        serializer = ProductListSerializer(popular_products, many=True)

        return Response({"stage": stage, "products": serializer.data})
