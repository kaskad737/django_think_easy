from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class YourTestCase(APITestCase):
    
    def setUp(self):
        # Создайте пользователя для тестирования
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Создайте URL-адреса для ваших представлений
        self.login_url = reverse('restaurantapiapp:token_obtain_pair')  
        self.secure_page_url = reverse('restaurantapiapp:visits_list')

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # Получите токен для пользователя
        token = self.obtain_token('testuser', 'testpassword')

        # Используйте токен для выполнения запроса к защищенному представлению
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

