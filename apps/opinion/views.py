from typing import cast

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.opinion.serializers import (
    GetOpinionSerializer,
    OpinionSerializer,
    GetQuestionSerializer,
    QuestionSerializer,
    GetCommentSerializer,
    CommentSerializer,
)
from apps.opinion.services.comment import CommentService
from apps.opinion.services.opinion import OpinionService
from apps.opinion.services.question import QuestionService
from apps.products.services.product import ProductService
from apps.users.models import User


def handle_like_action(service, request: Request, uuid: str) -> Response:
    """
    Универсальная функция для добавления или удаления лайков.
    """
    user = cast(User, request.user)
    opinion = service.get(uuid)
    service.add_or_remove_likes(user, opinion)
    return Response(
        {'data': {'likes': opinion.total_likes}}, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_handler(request: Request, uuid: str) -> Response:
    """
    Обработчик отслеживающий, что поставили лайк
    """
    like_target = request.query_params.get('for')

    if like_target == 'opinion':
        return handle_like_action(OpinionService, request, uuid)
    if like_target == 'comment':
        return handle_like_action(CommentService, request, uuid)
    if like_target == 'question':
        return handle_like_action(QuestionService, request, uuid)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_handler(request: Request, uuid: str) -> Response:
    """
    Обработчик отслеживающий, что поставили дизлайк
    """
    dislike_target = request.query_params.get('for')

    if dislike_target == 'opinion':
        return handle_like_action(OpinionService, request, uuid)
    if dislike_target == 'comment':
        return handle_like_action(CommentService, request, uuid)
    if dislike_target == 'question':
        return handle_like_action(QuestionService, request, uuid)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_opinion_handler(request: Request) -> Response:
    """
    Обработчик на получение или добавление отзыва на товар
    """
    product_uuid = request.query_params.get('product_uuid')
    if product_uuid is None:
        return Response(
            {'error': 'product_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    product = ProductService.get_only_uuid(product_uuid)

    if request.method == 'GET':
        opinions = OpinionService.filter(product)
        serializer = GetOpinionSerializer(opinions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = OpinionSerializer(
            data=request.data,
            context={'user': request.user, 'product': product},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_question_handler(request: Request) -> Response:
    """
    Обработчик на получение или добавление отзыва на товар
    """
    question_uuid = request.query_params.get('question_uuid')
    if question_uuid is None:
        return Response(
            {'error': 'product_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    question = ProductService.get_only_uuid(question_uuid)

    if request.method == 'GET':
        questions = QuestionService.filter(question)
        serializer = GetQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = QuestionSerializer(
            data=request.data,
            context={'user': request.user, 'question': question},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_comments_handler(request: Request) -> Response:
    """
    Обработчик на получение или добавление комментария на отзыв или вопрос
    """
    opinion_uuid = request.query_params.get('opinion_uuid')
    if opinion_uuid is None:
        return Response(
            {'error': 'opinion_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    opinion = OpinionService.get(opinion_uuid)

    if request.method == 'GET':
        comments = CommentService.filter(opinion)
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CommentSerializer(
            data=request.data,
            context={'user': request.user, 'opinion': opinion},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
