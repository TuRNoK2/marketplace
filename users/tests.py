from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# test проверка создания пользователя
class UserTest(TestCase):
    def test_create_and_list_users(self):

        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='123'
        )

        User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='456'
        )

        users = User.objects.all()
        print("\n📋 Список пользователей:")
        for user in users:
            print(f"👤 Username: {user.username}, Email: {user.email}")


        self.assertEqual(users.count(), 2)  # проверка

