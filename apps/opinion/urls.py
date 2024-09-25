from django.urls import path

from apps.opinion.views import (
    manage_opinion_handler,
    manage_comments_handler,
    manage_question_handler,
    like_handler,
    dislike_handler,
)

urlpatterns = [
    path('', manage_opinion_handler),
    path('comments/', manage_comments_handler),
    path('question/', manage_question_handler),
    path('like/', like_handler),
    path('dislike/', dislike_handler),
]
