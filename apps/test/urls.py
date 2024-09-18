from django.db import transaction
from django.http import HttpResponse
from django.urls import path

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)
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


@transaction.atomic
def catalog(request):
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
        name='Панель',
        product_image=None,
        specs='Панель',
        description='Панель',
        price=100.00,
        price_currency='RUB',
        stock_quantity=10,
        is_available=True,
        brand=brand,
    )
    product1 = Product.objects.create(
        name='Шкаф',
        product_image=None,
        specs='Шкаф',
        description='Шкаф',
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

    # Создаем главную категорию
    main_category = MainCategory.objects.create(
        name='Бытовая техника',
        description='Бытовая техника',
    )

    # Создаем подкатегорию
    sub_category = SubCategory.objects.create(
        main_category=main_category,
        name='Встраиваемая техника',
        description='Встраиваемая техника',
    )
    main_category.subcategories.add(sub_category)

    # Создаем разновидность техники
    product_variety = ProductVariety.objects.create(
        sub_category=sub_category,
        name='Варочные панели',
        description='Варочные панели',
    )
    product_variety1 = ProductVariety.objects.create(
        sub_category=sub_category,
        name='Духовные шкафы',
        description='Духовные шкафы',
    )
    sub_category.product_varietys.add(product_variety)
    sub_category.product_varietys.add(product_variety1)

    # Создаем тип техники
    product_type = ProductType.objects.create(
        product_variety=product_variety,
        name='Варочные панели электрические',
        description='Варочные панели электрические',
    )
    product_type1 = ProductType.objects.create(
        product_variety=product_variety,
        name='Духовные шкафы электрические',
        description='Духовные шкафы электрические',
    )
    product_variety.product_types.add(product_type)
    product_type.products.add(product)
    product_variety1.product_types.add(product_type1)

    # Создаем подтип продукта
    product_subtype = ProductSubtype.objects.create(
        product_type=product_type,
        name='Подтип продукта 1',
        description='Описание подтипа продукта 1',
    )
    product_type1.product_subtypes.add(product_subtype)
    product_subtype.products.add(product1)

    return HttpResponse('Каталог успешно создан')


urlpatterns = [
    path('test', test),
    path('catalog', catalog),
]
