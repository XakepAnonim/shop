from django.urls import path

from apps.custom_auth.views import (
    send_code_handler,
    verify_code_handler,
    change_password_handler,
    login_password_handler,
    reset_password_handler,
)

urlpatterns = [
    path('send', send_code_handler),
    path('verify', verify_code_handler),
    path('login', login_password_handler),
    path('password/change', change_password_handler),
    path('password/reset', reset_password_handler),
]
