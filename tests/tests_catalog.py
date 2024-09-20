import uuid

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)
from apps.catalog.views import CATEGORY_TYPES
from apps.users.models import User
from .tests_base import (
    user_data,
    main_category_data,
    sub_category_data,
    product_variety_data,
    product_type_data,
    product_subtype_data,
)


class CatalogTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Настройка переменных окружения
        """
        self.base_url = 'http://127.0.0.1:8000/api/v1/catalog/'
        self.client = APIClient()
        user = User.objects.create_user(**user_data)
        user_token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {user_token.access_token}'
        )

        # Создание тестовых данных
        self.main_category = MainCategory.objects.create(**main_category_data)
        self.sub_category = SubCategory.objects.create(
            mainCategory=self.main_category, **sub_category_data
        )
        self.product_variety = ProductVariety.objects.create(
            subCategory=self.sub_category, **product_variety_data
        )
        self.product_type = ProductType.objects.create(
            productVariety=self.product_variety, **product_type_data
        )
        self.product_subtype = ProductSubtype.objects.create(
            productType=self.product_type, **product_subtype_data
        )

    def test_get_catalog_success(self):
        """
        Автотест на получение всего каталога
        """
        url = f'{self.base_url}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['data']) > 0)

    def test_get_catalog_unauthorized(self):
        """
        Автотест на получение каталога для неавторизованного пользователя
        """
        self.client.credentials()
        url = f'{self.base_url}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_category_success(self):
        """
        Автотест на получение категории по uuid и slug для всех типов
        """
        for category_type in CATEGORY_TYPES:
            with self.subTest(category_type=category_type):
                match category_type:
                    case 'main':
                        url = f'{self.base_url}{self.main_category.uuid}/{self.main_category.slug}/?type={category_type}'
                    case 'sub':
                        url = f'{self.base_url}{self.sub_category.uuid}/{self.sub_category.slug}/?type={category_type}'
                    case 'variety':
                        url = f'{self.base_url}{self.product_variety.uuid}/{self.product_variety.slug}/?type={category_type}'
                    case 'type':
                        url = f'{self.base_url}{self.product_type.uuid}/{self.product_type.slug}/?type={category_type}'
                    case 'subtype':
                        url = f'{self.base_url}{self.product_subtype.uuid}/{self.product_subtype.slug}/?type={category_type}'

                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    response.data['data']['slug'], url.split('/')[-2]
                )

    def test_get_category_invalid_type(self):
        """
        Автотест на получение категории с невалидным типом
        """
        url = f'{self.base_url}{self.main_category.uuid}/{self.sub_category.slug}/?type=invalid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'], 'Invalid or missing category type'
        )

    def test_get_category_unauthorized(self):
        """
        Автотест на получение категории для неавторизованного пользователя
        """
        self.client.credentials()
        url = f'{self.base_url}{self.main_category.uuid}/{self.sub_category.slug}/?type=sub'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_category_not_found(self):
        """
        Автотест на получение категории по несуществующему uuid
        """
        url = (
            f'{self.base_url}{uuid.uuid4()}/{self.sub_category.slug}/?type=sub'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
