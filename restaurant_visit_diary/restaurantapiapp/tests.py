from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Restaurant
import json

class RestaurantssListTestCase(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')  
        cls.secure_page_url = reverse('restaurantapiapp:restaurants_list')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
    
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='test_restaurant_for_access', created_by=self.user2)

    def tearDown(self) -> None:
        self.restaurant.delete()

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # authentication test
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test that an authenticated user can create a restaurant.
        data = {
            'name': 'test_restaurant',
            'location': 'test_location',
            'cuisine_type': 'test_cousine'
            }
        response = self.client.post(self.secure_page_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test to see if the restaurant was actually created
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['results'][0]['name'], data['name'])


        # test that the user does not have access to the details of a restaurant he did not create
        response = self.client.get('http://testserver/api/restaurants/1/')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Not found.')


        


# class VisitsListTestCase(APITestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.user = User.objects.create_user(username='testuser', password='testpassword')
#         cls.login_url = reverse('restaurantapiapp:token_obtain_pair')  
#         cls.secure_page_url = reverse('restaurantapiapp:visits_list')

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.user.delete()
    
#     def setUp(self):
#         self.restaurant = Restaurant.objects.create(name='test_restaurant', created_by=self.user)

#     def tearDown(self) -> None:
#         self.restaurant.delete()

#     def obtain_token(self, username, password):
#         response = self.client.post(self.login_url, {'username': username, 'password': password})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         return response.data['access']

#     def test_authentication_with_token(self):
#         # Получите токен для пользователя
#         token = self.obtain_token('testuser', 'testpassword')

#         # Используйте токен для выполнения запроса к защищенному представлению
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         response = self.client.get(self.secure_page_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

