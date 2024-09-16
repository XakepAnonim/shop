from apps.users.models import User


def create_user(backend, response, *args, **kwargs):
    email = response.get('email')
    first_name = response.get('given_name')
    last_name = response.get('family_name')
    avatar = response.get('picture')
    approved_email = response.get('email_verified')

    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        avatar=avatar,
        approved_email=approved_email,
        phone_number=None,
    )
    user.has_usable_password()
