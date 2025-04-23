from django.test import TestCase
from .models import Cart, CartItem, Product
from django.contrib.auth.models import User


class CartModelTest(TestCase):
    def setUp(self):
        # Создание пользователя для теста
        self.user = User.objects.create_user(username="testuser", password="password")

        # Создание продукта для теста
        self.product = Product.objects.create(name="Test Product", price=100)

    def test_create_cart(self):
        # Создаем корзину для пользователя
        cart = Cart.objects.create(user=self.user)

        # Проверяем, что корзина создана и привязана к пользователю
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_add_item_to_cart(self):
        # Создаем корзину для пользователя
        cart = Cart.objects.create(user=self.user)

        # Добавляем товар в корзину
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Проверяем, что товар добавлен в корзину
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_remove_item_from_cart(self):
        # Создаем корзину и добавляем товар
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Удаляем товар из корзины
        cart_item.delete()

        # Проверяем, что корзина пуста
        self.assertEqual(cart.items.count(), 0)

    def test_get_total_price(self):
        # Создаем корзину и добавляем несколько товаров
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Проверяем общий стоимость товаров в корзине
        self.assertEqual(cart.get_total_price(), 200)
