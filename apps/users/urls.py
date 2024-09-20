from django.urls import path

from apps.users.views import (
    manage_user_handler,
    get_user_sessions_handler,
    close_session_handler,
    close_sessions_handler,
)

urlpatterns = [
    path('profile/', manage_user_handler),
    path('sessions/', get_user_sessions_handler),
    path('close/session/<str:authSSID>/', close_session_handler),
    path('close/sessions/', close_sessions_handler),
]
