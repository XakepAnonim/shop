from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OpinionSerializer
from .services.comment import OpinionCommentService
from .services.opinion import OpinionService
from ..products.services.product import ProductService


@api_view(['POST'])
def add_opinion(request):
    """
    Добавление отзыва на товар
    """
    product_uuid = request.query_params.get('product_uuid')
    product = ProductService.get_only_uuid(product_uuid)
    serializer = OpinionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_product_opinions(request):
    """
    Получение отзывов для товара
    """
    product_uuid = request.query_params.get('product_uuid')
    product = ProductService.get_only_uuid(product_uuid)
    opinions = OpinionService.filter(product)
    serializer = OpinionSerializer(opinions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def like_opinion(request, opinion_uuid):
    opinion = OpinionService.get(opinion_uuid)
    OpinionService.add_or_remove_likes(request.user, opinion)
    return Response({'data': {
        'likes': opinion.total_likes
    }}, status=status.HTTP_200_OK)


@api_view(['POST'])
def dislike_opinion(request, opinion_uuid):
    opinion = OpinionService.get(opinion_uuid)
    OpinionService.add_or_remove_likes(request.user, opinion)
    return Response({'data': {
        'likes': opinion.total_likes
    }}, status=status.HTTP_200_OK)


@api_view(['POST'])
def like_comment(request, opinion_comment_uuid):
    opinion = OpinionCommentService.get(opinion_comment_uuid)
    OpinionCommentService.add_or_remove_likes(request.user, opinion)
    return Response({'data': {
        'likes': opinion.total_likes
    }}, status=status.HTTP_200_OK)


@api_view(['POST'])
def dislike_comment(request, opinion_comment_uuid):
    opinion = OpinionCommentService.get(opinion_comment_uuid)
    OpinionCommentService.add_or_remove_likes(request.user, opinion)
    return Response({'data': {
        'likes': opinion.total_likes
    }}, status=status.HTTP_200_OK)
