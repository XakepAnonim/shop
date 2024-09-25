from uuid import UUID

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import AuthUserSerializer, UpdateUserSerializer
from apps.users.services.session import SessionService
from apps.users.services.user import UserService


def get_user_handler(request: Request, user: User) -> Response:
    """
    Обработчик получения профиля пользователя
    """
    serializer = AuthUserSerializer(user)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


def update_data_user_handler(request: Request, user: User) -> Response:
    """
    Обработчик обновления профиля пользователя
    """
    serializer = UpdateUserSerializer(
        data=request.data, instance=user, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        responses=AuthUserSerializer,
        description='Получение профиля пользователя',
        summary='Получение профиля пользователя',
        tags=['Пользователь'],
    ),
    patch=extend_schema(
        request=UpdateUserSerializer,
        responses=UpdateUserSerializer,
        description='Обновление профиля пользователя',
        summary='Обновление профиля пользователя',
        tags=['Пользователь'],
    ),
)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def manage_user_handler(request: Request) -> Response:
    """
    Менеджер взаимодействия с пользователем
    """
    if isinstance(request.user, User) and isinstance(request.user.uuid, UUID):
        user = UserService.get(str(request.user.uuid))
        if request.method == 'GET':
            return get_user_handler(request, user)
        if request.method == 'PATCH':
            return update_data_user_handler(request, user)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={
        200: OpenApiResponse(
            description='Сеансы пользователя',
        )
    },
    summary='Получение сеансов пользователя',
    description='Получение сеансов пользователя',
    tags=['Сессия'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_sessions_handler(request: Request) -> Response:
    """
    Получение сеансов пользователя
    """
    if isinstance(request.user, User):
        sessions = SessionService.filter_by_user(request.user)
        session_data = []
        for session in sessions:
            session_data.append(
                {
                    'authSSID': session.authSSID,
                    'placeID': {
                        'deviceType': session.deviceType,
                        'deviceName': session.deviceName,
                        'os': session.os,
                        'browser': session.browser,
                        'ip': session.ip,
                        'cityName': '',
                        'installationId': None,
                    },
                    'createdAt': session.createdAt.isoformat(),
                    'country': session.country,
                    'isCurrent': session.isCurrent,
                }
            )
        return Response({'data': session_data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: OpenApiResponse(description='No Content')},
    description='Отключение сеанса пользователя',
    summary='Отключение сеанса пользователя',
    examples=[
        OpenApiExample(
            'authSSID',
            description='ID сеанса',
        ),
    ],
    tags=['Сессия'],
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def close_session_handler(request: Request, authSSID: str) -> Response:
    """
    Отключение сеанса пользователя
    """
    SessionService.delete_session(authSSID)
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    responses={204: OpenApiResponse(description='No Content')},
    description='Отключение неактивных сеансов пользователя',
    summary='Отключение неактивных сеансов пользователя',
    tags=['Сессия'],
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def close_sessions_handler(request: Request) -> Response:
    """
    Отключение неактивных сеансов пользователя
    """
    SessionService.delete_sessions()
    return Response(status=status.HTTP_204_NO_CONTENT)
