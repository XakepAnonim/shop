import uuid
from user_agents import parse

from apps.users.models import UserSession


def create_user_session(request, user, **kwargs):
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
