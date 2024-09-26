from typing import cast

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    extend_schema_view,
    OpenApiExample,
)
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
    obj = service.get(uuid)
    service.add_or_remove_likes(user, obj)
    return Response(
        {'data': {'likes': obj.total_likes}}, status=status.HTTP_200_OK
    )


def handle_dislike_action(service, request: Request, uuid: str) -> Response:
    """
    Универсальная функция для добавления или удаления дизлайков.
    """
    user = cast(User, request.user)
    obj = service.get(uuid)
    service.add_or_remove_dislikes(user, obj)
    return Response(
        {'data': {'likes': obj.total_likes}}, status=status.HTTP_200_OK
    )


@extend_schema(
    description='Добавление лайка к отзыву, комментарию или вопросу',
    summary='Поставить лайк',
    tags=['Лайки'],
    responses={
        200: OpenApiResponse(
            description='Успешный ответ с количеством лайков'
        ),
        400: OpenApiResponse(description='Ошибка при отсутствии параметров'),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_handler(request: Request) -> Response:
    """
    Обработчик отслеживающий, что поставили лайк
    """
    like_target: int = request.query_params.get('for')
    uuid: str = request.query_params.get('uuid')

    if not like_target:
        return Response(
            {'error': 'like_target is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not uuid:
        return Response(
            {'error': 'uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    match like_target:
        case 'opinion':
            return handle_like_action(OpinionService, request, uuid)
        case 'comment':
            return handle_like_action(CommentService, request, uuid)
        case 'question':
            return handle_like_action(QuestionService, request, uuid)


@extend_schema(
    description='Добавление дизлайка к отзыву, комментарию или вопросу',
    summary='Поставить дизлайк',
    tags=['Дизлайки'],
    examples=[
        OpenApiExample(
            'dislike_target',
            description='Куда дизлайк',
        ),
    ],
    responses={
        200: OpenApiResponse(
            description='Успешный ответ с количеством лайков'
        ),
        400: OpenApiResponse(description='Ошибка при отсутствии параметров'),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_handler(request: Request) -> Response:
    """
    Обработчик отслеживающий, что поставили дизлайк
    """
    dislike_target: int = request.query_params.get('for')
    uuid: str = request.query_params.get('uuid')

    if dislike_target is None:
        return Response(
            {'error': 'dislike_target is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if uuid is None:
        return Response(
            {'error': 'uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    match dislike_target:
        case 'opinion':
            return handle_dislike_action(OpinionService, request, uuid)
        case 'comment':
            return handle_dislike_action(CommentService, request, uuid)
        case 'question':
            return handle_dislike_action(QuestionService, request, uuid)


@extend_schema_view(
    get=extend_schema(
        responses=GetOpinionSerializer,
        description='Получение отзыва на товар',
        summary='Получение отзыва на товар',
        tags=['Отзыв'],
    ),
    post=extend_schema(
        request=OpinionSerializer,
        responses=OpinionSerializer,
        description='Добавление отзыва на товар',
        summary='Добавление отзыва на товар',
        tags=['Отзыв'],
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        responses=GetQuestionSerializer,
        description='Получение вопроса на товар',
        summary='Получение вопроса на товар',
        tags=['Вопрос'],
    ),
    post=extend_schema(
        request=QuestionSerializer,
        responses=QuestionSerializer,
        description='Добавление вопроса на товар',
        summary='Добавление вопроса на товар',
        tags=['Вопрос'],
    ),
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_question_handler(request: Request) -> Response:
    """
    Обработчик на получение или добавление вопроса на товар
    """
    product_uuid = request.query_params.get('product_uuid')
    if product_uuid is None:
        return Response(
            {'error': 'product_uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    product = ProductService.get_only_uuid(product_uuid)

    if request.method == 'GET':
        questions = QuestionService.filter(product)
        serializer = GetQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = QuestionSerializer(
            data=request.data,
            context={'user': request.user, 'product': product},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        responses=GetCommentSerializer,
        description='Получение комментария на отзыва или вопрос',
        summary='Получение комментария на отзыва или вопрос',
        tags=['Комментарий'],
    ),
    post=extend_schema(
        request=CommentSerializer,
        responses=CommentSerializer,
        description='Добавление комментария на отзыв или вопрос',
        summary='Добавление комментария на отзыв или вопрос',
        tags=['Комментарий'],
    ),
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_comments_handler(request: Request) -> Response:
    """
    Обработчик на получение или добавление комментария на отзыв или вопрос
    """
    obj_uuid = request.query_params.get('uuid')
    obj_target = request.query_params.get('for')
    opinion = None
    question = None
    context = None

    if obj_uuid is None:
        return Response(
            {'error': 'uuid is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if obj_target is None:
        return Response(
            {'error': 'for is missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if obj_target == 'opinion':
        opinion = OpinionService.get(obj_uuid)

    elif obj_target == 'question':
        question = QuestionService.get(obj_uuid)

    if request.method == 'GET':
        if obj_target == 'opinion':
            comments = CommentService.filter_opinion(opinion)
            serializer = GetCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif obj_target == 'question':
            comments = CommentService.filter_question(question)
            serializer = GetCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        if obj_target == 'opinion':
            context = {'user': request.user, 'opinion': opinion}

        elif obj_target == 'question':
            context = {'user': request.user, 'question': question}

        serializer = CommentSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
