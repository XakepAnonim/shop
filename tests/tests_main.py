from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.main.models import Brand, Company
from apps.products.models import Product
from apps.users.models import User
from .tests_base import (
    user_data,
    company_data,
    brand_data,
    product_data,
)


class BrandTestCase(APITestCase):
    def setUp(self) -> None:
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

        # Создание компании и бренда для тестов
        self.company = Company.objects.create(**company_data)
        self.brand = Brand.objects.create(company=self.company, **brand_data)
        self.product = Product.objects.create(brand=self.brand, **product_data)

    def test_get_brand(self):
        """
        Тест на получение информации о бренде
        """
        output_brand_data = {
            'uuid': str(self.brand.uuid),
            'name': 'Test Brand',
            'description': 'Test Brand Description',
            'image': None,
            'products': [
                {
                    'uuid': str(self.product.uuid),
                    'name': 'Product 1',
                    'image': None,
                    'specs': 'Specs 1',
                    'price': '100.00',
                    'priceCurrency': 'RUB',
                    'stockQuantity': 10,
                    'isAvailable': True,
                }
            ],
        }

        url = f'{self.base_url}brand/{self.brand.name}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], output_brand_data)

    def test_get_brand_not_found(self):
        """
        Тест на получение бренда, который не существует
        """
        url = f'{self.base_url}brand/blala/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
