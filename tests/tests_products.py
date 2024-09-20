from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.main.models import Company, Brand
from apps.products.models import Product, Characteristic, CharacteristicGroup
from apps.users.models import User
from tests.tests_base import (
    user_data,
    company_data,
    brand_data,
    product_data,
    characteristic_data,
    characteristic_group_data,
)


class ProductAPITests(APITestCase):
    def setUp(self):
        """
        Настройка переменных окружения и создание тестовых данных
        """
        self.base_url = 'http://127.0.0.1:8000/api/v1/'
        self.client = APIClient()
        user = User.objects.create_user(**user_data)
        user_token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {user_token.access_token}'
        )

        self.company = Company.objects.create(**company_data)
        self.brand = Brand.objects.create(company=self.company, **brand_data)
        self.product = Product.objects.create(brand=self.brand, **product_data)
        self.characteristic_group = CharacteristicGroup.objects.create(
            product=self.product, **characteristic_group_data
        )
        self.characteristic = Characteristic.objects.create(
            group=self.characteristic_group, **characteristic_data
        )

    def test_get_product_success(self):
        output_product_data = {
            'uuid': str(self.product.uuid),
            'name': 'Product 1',
            'image': None,
            'specs': 'Specs 1',
            'description': 'Description 1',
            'sku': self.product.sku,
            'price': '100.00',
            'priceCurrency': 'RUB',
            'stockQuantity': 10,
            'isAvailable': True,
            'brand': {
                'uuid': str(self.brand.uuid),
                'name': 'Test Brand',
            },
            'characteristics': [
                {
                    'name': 'CharacteristicGroup 1',
                    'characteristic': [
                        {'title': 'Title 1', 'value': 'Value 1'}
                    ],
                }
            ],
        }

        url = (
            f'{self.base_url}products/{self.product.uuid}/{self.product.slug}/'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], output_product_data)

    def test_get_product_not_found(self):
        url = f'{self.base_url}products/123/blala/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_unauthenticated(self):
        self.client.credentials()
        url = (
            f'{self.base_url}products/{self.product.uuid}/{self.product.slug}/'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
