from django.http import HttpResponse
from django.urls import path

from apps.main.models import (
    Company,
    Brand,
)
from apps.products.models import Product, CharacteristicGroup, Characteristic


def test(request):
    # Создаем компанию
    company = Company.objects.create(
        name='Компания 1',
        description='Описание компании 1',
    )

    # Создаем бренд
    brand = Brand.objects.create(
        name='Бренд 1',
        company=company,
    )

    # Создаем продукт
    product = Product.objects.create(
        name='Продукт 1',
        product_image=None,
        specs='Тех. характеристики продукта 1',
        description='Описание продукта 1',
        price=100.00,
        price_currency='RUB',
        stock_quantity=10,
        is_available=True,
        brand=brand,
    )

    # Создаем группу характеристик
    characteristic_group = CharacteristicGroup.objects.create(
        name='Группа характеристик 1',
        product=product,
    )

    # Создаем характеристику
    characteristic = Characteristic.objects.create(
        group=characteristic_group,
        title='Характеристика 1',
        value='Значение характеристики 1',
    )

    # Связываем характеристику с группой
    characteristic_group.characteristics.add(characteristic)

    return HttpResponse('Объекты успешно созданы')


urlpatterns = [path('test', test)]
