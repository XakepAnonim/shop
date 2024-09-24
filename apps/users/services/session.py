import uuid

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from user_agents import parse

from apps.users.models import UserSession, User


class SessionService:
    @staticmethod
    def get(authSSID: str) -> UserSession:
        """
        Получение сеанса
        """
        session = get_object_or_404(UserSession, authSSID=authSSID)
        return session

    @staticmethod
    def filter_by_user(user: User) -> QuerySet[UserSession]:
        """
        Получение сеанса фильтруя по пользователю
        """
        sessions = UserSession.objects.filter(user=user)
        return sessions

    @staticmethod
    def filter_is_current() -> QuerySet[UserSession]:
        """
        Получение сеанса фильтруя по не активности
        """
        sessions = UserSession.objects.filter(isCurrent=False)
        return sessions

    @staticmethod
    def create(request: Request, user: User) -> None:
        """
        Создание сеанса
        """
        user_agent_string = request.META.get(
            'HTTP_USER_AGENT', '<unknown user agent>'
        )
        user_agent = parse(user_agent_string)
        UserSession.objects.create(
            user=user,
            authSSID=str(uuid.uuid4().hex),
            deviceType=user_agent.device.family or 'Desktop',
            deviceName=user_agent.device.model or '<unknown>',
            os=f'{user_agent.os.family} {user_agent.os.version_string}',
            browser=f'{user_agent.browser.family} {user_agent.browser.version_string}',
            ip=request.META.get('REMOTE_ADDR', '<unknown IP>'),
            userAgent=user_agent_string,
            country=request.headers.get('CF-IPCountry', 'unknown'),
        )

    @classmethod
    def delete_session(cls, authSSID: str) -> None:
        """
        Отключение сеанса
        """
        session = cls.get(authSSID)
        session.delete()

    @classmethod
    def delete_sessions(cls) -> None:
        """
        Отключение сеансов
        """
        sessions = cls.filter_is_current()
        sessions.delete()
