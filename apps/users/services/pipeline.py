def fill_missing_user_google_data(backend, details, response, *args, **kwargs):
    """
    Заполняет недостающие данные пользователя перед созданием.
    """
    first_name = response.get('given_name') or details.get('first_name')
    last_name = response.get('family_name') or details.get('last_name')
    phone = response.get('phone') or ''

    details['first_name'] = first_name
    details['last_name'] = last_name
    details['phone_number'] = phone

    kwargs['details'] = details
