from django.db import transaction
from django.http import HttpResponse
from django.urls import path
from rest_framework.request import Request

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)
from apps.main.models import Company, Brand
from apps.products.models import Product, CharacteristicGroup, Characteristic


@transaction.atomic
def catalog(request: Request) -> HttpResponse:
    # Получаем или создаем компанию
    company, _ = Company.objects.get_or_create(
        name='Компания 1',
        defaults={'description': 'Описание компании 1'},
    )

    # Получаем или создаем бренд
    brand, _ = Brand.objects.get_or_create(
        name='Бренд 1',
        company=company,
    )

    # Кэширование продуктов для избежания дублирующих запросов
    existing_products = {
        p.name: p for p in Product.objects.filter(name__in=['Панель', 'Шкаф'])
    }
    products_data = [
        {'name': 'Панель', 'specs': 'Панель', 'description': 'Панель'},
        {'name': 'Шкаф', 'specs': 'Шкаф', 'description': 'Шкаф'},
    ]
    products = []
    for data in products_data:
        if data['name'] in existing_products:
            product = existing_products[data['name']]
        else:
            product = Product.objects.create(
                name=data['name'],
                image=None,
                specs=data['specs'],
                description=data['description'],
                price=100.00,
                priceCurrency='RUB',
                stockQuantity=10,
                isAvailable=True,
                brand=brand,
            )
        products.append(product)

    # Кэширование групп характеристик
    characteristic_group, _ = CharacteristicGroup.objects.get_or_create(
        name='Группа характеристик 1',
        product=products[0],
    )

    # Кэширование характеристик
    characteristic, _ = Characteristic.objects.get_or_create(
        group=characteristic_group,
        title='Характеристика 1',
        defaults={'value': 'Значение характеристики 1'},
    )

    # Главная категория и подкатегория
    main_category, _ = MainCategory.objects.get_or_create(
        name='Бытовая техника',
    )

    sub_category, _ = SubCategory.objects.get_or_create(
        mainCategory=main_category,
        name='Встраиваемая техника',
    )

    # Кэширование разновидностей техники
    existing_varieties = {
        v.name: v
        for v in ProductVariety.objects.filter(
            name__in=['Варочные панели', 'Духовные шкафы']
        )
    }
    product_varieties_data = ['Варочные панели', 'Духовные шкафы']
    product_varieties = []
    for variety_name in product_varieties_data:
        if variety_name in existing_varieties:
            product_variety = existing_varieties[variety_name]
        else:
            product_variety = ProductVariety.objects.create(
                subCategory=sub_category,
                name=variety_name,
            )
        product_varieties.append(product_variety)

    # Кэширование типов техники
    existing_types = {
        t.name: t
        for t in ProductType.objects.filter(
            name__in=[
                'Варочные панели электрические',
                'Духовные шкафы электрические',
            ]
        )
    }
    product_types_data = [
        {
            'name': 'Варочные панели электрические',
            'variety': product_varieties[0],
        },
        {
            'name': 'Духовные шкафы электрические',
            'variety': product_varieties[1],
        },
    ]
    product_types = []
    for data in product_types_data:
        if data['name'] in existing_types:
            product_type = existing_types[data['name']]
        else:
            product_type = ProductType.objects.create(
                productVariety=data['variety'],
                name=data['name'],
            )
        product_types.append(product_type)

    # Создаем или получаем подтип продукта
    product_subtype, _ = ProductSubtype.objects.get_or_create(
        productType=product_types[0],
        name='Подтип продукта 1',
    )

    # Добавляем продукты в соответствующие типы/подтипы
    product_types[0].products_in_type.add(products[0])
    product_subtype.products_in_subtype.add(products[1])

    return HttpResponse('Каталог успешно создан')


urlpatterns = [
    path('catalog/', catalog),
]
