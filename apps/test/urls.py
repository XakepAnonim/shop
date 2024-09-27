import random

from django.db import transaction
from django.http import HttpResponse
from django.urls import path
from faker import Faker
from django.utils.text import slugify
from unidecode import unidecode
from rest_framework.request import Request

from apps.cart.models import Cart, CartItem
from apps.cart.services.cart import CartService
from apps.catalog.models import Category
from apps.main.models import Company, Brand
from apps.opinion.models import Opinion, Question, Comment, Grades
from apps.products.models import (
    Product,
    CharacteristicGroup,
    Characteristic,
    WishlistProduct,
)
from apps.users.models import Permission, User

fake = Faker('ru_RU')


@transaction.atomic
def create_permissions(user):
    permissions = [
        {
            'name': 'Доступ к админке',
            'codename': 'access_admin',
            'role': 'admin',
        },
        {
            'name': 'Управление продуктами',
            'codename': 'manage_products',
            'role': 'admin',
        },
        {
            'name': 'Просмотр заказов',
            'codename': 'view_orders',
            'role': 'user',
        },
        {
            'name': 'Добавление отзывов',
            'codename': 'add_reviews',
            'role': 'user',
        },
    ]
    permission_objs = [Permission(**perm) for perm in permissions]
    Permission.objects.bulk_create(permission_objs)
    user.permissions.add(*permission_objs[:2])  # Пример добавления разрешений


@transaction.atomic
def create_companies_and_brands(n=5):
    companies = []
    brands = []
    for _ in range(n):
        company = Company(
            name=fake.company(), description=fake.text(max_nb_chars=200)
        )
        companies.append(company)
    Company.objects.bulk_create(companies)

    all_companies = Company.objects.all()
    for _ in range(n * 3):  # Предположим, 3 бренда на компанию
        brand = Brand(
            name=fake.company_suffix(),
            description=fake.text(max_nb_chars=200),
            company=random.choice(all_companies),
        )
        brands.append(brand)
    Brand.objects.bulk_create(brands)


@transaction.atomic
def create_categories(n=20):
    for _ in range(n):
        category = Category(
            name=fake.unique.word().capitalize(),
            parent=random.choice(Category.objects.all())
            if Category.objects.exists() and random.choice([True, False])
            else None,
        )
        category.save()


@transaction.atomic
def create_products(n=50):
    products = []
    existing_slugs = set(Product.objects.values_list('slug', flat=True))

    for _ in range(n):
        brand = random.choice(Brand.objects.all())
        category = random.choice(Category.objects.all())
        name = fake.word().capitalize() + ' ' + fake.word().capitalize()

        # Генерация уникального slug
        base_slug = slugify(unidecode(name))
        unique_slug = base_slug
        suffix = 1
        while unique_slug in existing_slugs:
            unique_slug = f'{base_slug}-{suffix}'
            suffix += 1
        existing_slugs.add(unique_slug)

        product = Product(
            name=name,
            slug=unique_slug,
            specs=fake.text(max_nb_chars=300),
            description=fake.text(max_nb_chars=500),
            sku=random.randint(100000, 999999),
            price=random.randint(1000, 100000),
            priceCurrency='RUB',
            stockQuantity=random.randint(0, 1000),
            isAvailable=random.choice([True, False]),
            brand=brand,
            category=category,
        )
        products.append(product)
    Product.objects.bulk_create(products)

    # Создание характеристик для продуктов
    all_products = Product.objects.all()
    char_groups = []
    characteristics = []
    for product in all_products:
        group = CharacteristicGroup(
            name='Основные характеристики', product=product
        )
        char_groups.append(group)
    CharacteristicGroup.objects.bulk_create(char_groups)

    all_char_groups = CharacteristicGroup.objects.all()
    for group in all_char_groups:
        for _ in range(5):  # 5 характеристик на группу
            characteristic = Characteristic(
                title=fake.word().capitalize(), value=fake.word(), group=group
            )
            characteristics.append(characteristic)
    Characteristic.objects.bulk_create(characteristics)


@transaction.atomic
def create_users(n=10):
    users = []
    for _ in range(n):
        user = User(
            email=fake.unique.email(),
            firstName=fake.first_name(),
            lastName=fake.last_name(),
            isStaff=random.choice([True, False]),
        )
        user.set_password('password123')  # Устанавливаем пароль
        users.append(user)
    User.objects.bulk_create(users)
    # Добавление разрешений для администраторов
    admin_users = User.objects.filter(isStaff=True)
    for user in admin_users:
        create_permissions(user)


@transaction.atomic
def create_cart_and_wishlist():
    users = User.objects.all()
    products = list(
        Product.objects.all()
    )  # Преобразуем QuerySet в список для выборки
    for user in users:
        # Создание корзины с вероятностью 50%
        if random.choice([True, False]):
            cart = Cart.objects.create(user=user)

            # Определяем количество элементов в корзине (например, от 1 до 5)
            num_items = random.randint(1, 5)

            # Выбираем уникальные продукты для корзины
            sampled_products = random.sample(
                products, k=min(num_items, len(products))
            )

            for product in sampled_products:
                # Определяем количество для каждого продукта (например, от 1 до 5)
                quantity = random.randint(1, 5)

                # Создаем CartItem для выбранного продукта и добавляем его в корзину
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity,
                )

            # Обновляем общую стоимость корзины с учетом новых элементов
            CartService.update_cart_totals(cart)

        # Создание списка желаемых товаров (Wishlist) с вероятностью 50%
        if random.choice([True, False]):
            wishlist = WishlistProduct.objects.create(
                count=random.randint(1, 3),
                total_price=random.randint(1000, 30000),
                user=user,
            )
            # Выбираем уникальные продукты для Wishlist
            sampled_products = random.sample(
                products, k=min(random.randint(1, 3), len(products))
            )
            wishlist.products.add(*sampled_products)


@transaction.atomic
def create_opinions_questions_comments_grades(n=100):
    users = User.objects.all()
    products = Product.objects.all()
    opinions = []
    questions = []
    comments = []
    grades = []

    for _ in range(n):
        user = random.choice(users)
        product = random.choice(products)
        opinion = Opinion(
            user=user,
            advantages=fake.sentence(),
            disadvantages=fake.sentence(),
            commentary=fake.paragraph(),
            periods=fake.random_element(
                elements=('Не более года', 'Более года', 'Менее полугода')
            ),
            product=product,
        )
        opinions.append(opinion)

    Opinion.objects.bulk_create(opinions)
    all_opinions = Opinion.objects.all()

    for _ in range(n):
        user = random.choice(users)
        product = random.choice(products)
        question = Question(
            user=user,
            title=fake.sentence(nb_words=6),
            text=fake.paragraph(),
            product=product,
        )
        questions.append(question)
    Question.objects.bulk_create(questions)

    for opinion in all_opinions:
        for _ in range(random.randint(0, 3)):  # до 3 комментариев на отзыв
            comment = Comment(
                user=random.choice(users),
                text=fake.sentence(),
                opinion=opinion,
            )
            comments.append(comment)
    Comment.objects.bulk_create(comments)

    for opinion in all_opinions:
        grade = Grades(
            title=fake.word().capitalize(),
            grade=random.randint(1, 5),
            opinion=opinion,
        )
        grades.append(grade)
    Grades.objects.bulk_create(grades)


@transaction.atomic
def shop(request: Request) -> HttpResponse:
    # Создание пользователей
    create_users(n=20)

    # Создание компаний и брендов
    create_companies_and_brands(n=10)

    # Создание категорий
    create_categories(n=20)

    # Создание продуктов и их характеристик
    create_products(n=100)

    # Создание корзин и избранного
    create_cart_and_wishlist()

    # Создание отзывов, вопросов, комментариев и оценок
    create_opinions_questions_comments_grades(n=200)

    return HttpResponse(
        'Каталог успешно расширен с большим количеством объектов.'
    )


urlpatterns = [
    path('shop/', shop),
]
