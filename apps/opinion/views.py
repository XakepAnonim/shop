from typing import cast

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import OpinionSerializer
from .services.comment import OpinionCommentService
from .services.opinion import OpinionService
from ..products.services.product import ProductService
from ..users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_opinion(request: Request) -> Response:
    """
    Добавление отзыва на товар
    """
    product_uuid = request.query_params.get('product_uuid')

    if product_uuid is None:
        return Response(
            {'error': 'product_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    product = ProductService.get_only_uuid(product_uuid)
    serializer = OpinionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_opinions(request: Request) -> Response:
    """
    Получение отзывов для товара
    """
    product_uuid = request.query_params.get('product_uuid')

    if product_uuid is None:
        return Response(
            {'error': 'product_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    product = ProductService.get_only_uuid(product_uuid)
    opinions = OpinionService.filter(product)
    serializer = OpinionSerializer(opinions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_opinion(request: Request, opinion_uuid: str) -> Response:
    user = cast(User, request.user)
    opinion = OpinionService.get(opinion_uuid)
    OpinionService.add_or_remove_likes(user, opinion)
    return Response(
        {'data': {'likes': opinion.total_likes}}, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_opinion(request: Request, opinion_uuid: str) -> Response:
    user = cast(User, request.user)
    opinion = OpinionService.get(opinion_uuid)
    OpinionService.add_or_remove_likes(user, opinion)
    return Response(
        {'data': {'likes': opinion.total_likes}}, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request: Request, opinion_comment_uuid: str) -> Response:
    user = cast(User, request.user)
    opinion = OpinionCommentService.get(opinion_comment_uuid)
    OpinionCommentService.add_or_remove_likes(user, opinion)
    return Response(
        {'data': {'likes': opinion.total_likes}}, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_comment(request: Request, opinion_comment_uuid: str) -> Response:
    user = cast(User, request.user)
    opinion = OpinionCommentService.get(opinion_comment_uuid)
    OpinionCommentService.add_or_remove_likes(user, opinion)
    return Response(
        {'data': {'likes': opinion.total_likes}}, status=status.HTTP_200_OK
    )
