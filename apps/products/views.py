import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from rest_framework.response import Response
from apps.products.serializers import ProductSerializer
from apps.products.services.product import ProductService


@api_view(['GET'])
def get_product(request: Request, uuid: uuid.uuid4, slug) -> Response:
    product = ProductService.get(uuid, slug)
    serializer = ProductSerializer(product)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
