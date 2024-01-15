from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Restaurant

class VisitsListTestCase(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')  
        cls.secure_page_url = reverse('restaurantapiapp:visits_list')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
    
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='test_restaurant', created_by=self.user)

    def tearDown(self) -> None:
        self.restaurant.delete()

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

