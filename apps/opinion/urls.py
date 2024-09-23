from django.urls import path

from apps.opinion.views import (
    get_product_opinions,
    add_opinion,
    like_opinion,
    dislike_opinion
)

urlpatterns = [
    path('', get_product_opinions),
    path('add/', add_opinion),
    path('like/', like_opinion),
    path('dislike/', dislike_opinion),
    path('comment/like/', like_opinion),
    path('comment/dislike/', dislike_opinion),
]
