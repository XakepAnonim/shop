from apps.custom_auth.services.session import create_user_session
from apps.users.models import User


def create_user(request, backend, response, *args, **kwargs):
    email = response.get('email')
    first_name = response.get('given_name')
    last_name = response.get('family_name')
    avatar = response.get('picture')
    approved_email = response.get('email_verified')

    user = User.objects.create_user(
        email=email,
        firstName=first_name,
        lastName=last_name,
        avatar=avatar,
        approvedEmail=approved_email,
        phoneNumber=None,
    )
    user.has_usable_password()
    create_user_session(request, user, **kwargs)
