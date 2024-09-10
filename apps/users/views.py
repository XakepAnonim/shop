from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.serializers import AuthUserSerializer, UpdateUserSerializer
from apps.users.services.user import UserService


def get_user(request: Request, user) -> Response:
    serializer = AuthUserSerializer(user)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


def update_data_user(request: Request, user) -> Response:
    serializer = UpdateUserSerializer(
        data=request.data, instance=user, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def manage_user_handler(request: Request) -> Response:
    user = UserService.get(request.user.uuid)
    if request.method == 'GET':
        return get_user(request, user)
    if request.method == 'PATCH':
        return update_data_user(request, user)
