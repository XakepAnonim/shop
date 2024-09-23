from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OpinionSerializer
from .models import Product, Opinion


@api_view(['POST'])
def add_opinion(request):
    """
    Добавление отзыва на товар
    """
    product_uuid = request.query_params.get('product_uuid')
    product = Product.objects.get(uuid=product_uuid)
    serializer = OpinionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_product_opinions(request):
    """
    Получение отзывов для товара
    """
    product_uuid = request.query_params.get('product_uuid')
    product = Product.objects.get(uuid=product_uuid)
    opinions = Opinion.objects.filter(product=product)
    serializer = OpinionSerializer(opinions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def like_opinion(request, opinion_id):
    opinion = Opinion.objects.get(id=opinion_id)
    if request.user in opinion.likes.all():
        opinion.likes.remove(request.user)
    else:
        opinion.likes.add(request.user)
        opinion.dislikes.remove(request.user)
    return Response(
        {
            'total_likes': opinion.total_likes(),
            'total_dislikes': opinion.total_dislikes(),
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
def dislike_opinion(request, opinion_id):
    opinion = Opinion.objects.get(id=opinion_id)
    if request.user in opinion.dislikes.all():
        opinion.dislikes.remove(request.user)
    else:
        opinion.dislikes.add(request.user)
        opinion.likes.remove(request.user)
    return Response(
        {
            'total_likes': opinion.total_likes(),
            'total_dislikes': opinion.total_dislikes(),
        },
        status=status.HTTP_200_OK,
    )
