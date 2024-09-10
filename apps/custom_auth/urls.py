from django.urls import path

from apps.custom_auth.views import (
    send_code_handler,
    verify_code_handler,
    change_password_handler,
)

urlpatterns = [
    path('send', send_code_handler),
    path('verify', verify_code_handler),
    path('password/reset', change_password_handler),
]
