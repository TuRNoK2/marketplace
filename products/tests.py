from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Category


class ProductCreateTest(TestCase):

    def setUp(self):
        self.user_seller = get_user_model().objects.create_user(
            username='seller',
            password='password123',
            role='seller',
        )


        self.category = Category.objects.create(name='Electronics')

        self.url = reverse('product_create')

    def test_create_product_as_seller(self):
        # Логинимся как продавец
        self.client.login(username='seller', password='password123')

        # Данные для создания продукта
        product_data = {
            'name': 'New Product',
            'description': 'A very cool product',
            'price': 100.00,
            'category': self.category.id,
            'image': None,
        }

        # Отправляем POST-запрос для создания продукта
        response = self.client.post(self.url, data=product_data)

        # Проверка, что продукт был создан
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)  # Проверяем, что продукт был создан

        # Проверяем, что данные продукта совпадают с тем, что мы отправили
        product = Product.objects.first()
        self.assertEqual(product.name, 'New Product')
        self.assertEqual(product.description, 'A very cool product')
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.category, self.category)

    def test_create_product_as_non_seller(self):
        user_buyer = get_user_model().objects.create_user(
            username='buyer',
            password='password123',
            role='buyer',
        )


        self.client.login(username='buyer', password='password123')


        response = self.client.post(self.url, data={})

        # Проверяем, что покупатель не может создать продукт
        self.assertEqual(response.status_code, 403)
