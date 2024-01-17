import json
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from .models import Restaurant, Visit


class RestaurantsListTestCase(APITestCase):
    fixtures = [
        'user-fixtures.json',
        'restaurant-fixture.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user1 = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
            )
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')
        cls.secure_page_url = reverse('restaurantapiapp:restaurants_list')
        cls.restaurant = Restaurant.objects.create(
            name='test_restaurant_for_access',
            created_by=cls.user2
            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user1.delete()
        cls.user2.delete()
        cls.restaurant.delete()

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {
            'username': username,
            'password': password}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # authentication test
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_restaurant(self):
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # test that an authenticated user can create a restaurant
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

        # test that the user does not have access to the details
        # of a restaurant he did not create
        response = self.client.get(reverse(
            'restaurantapiapp:restaurant_detail',
            args=[self.restaurant.pk]
            ))
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Not found.')

    def test_anonymous_user_deny_access(self):
        # authentication test for anonymous user
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RestaurantDetailsTestCase(APITestCase):
    fixtures = [
        'user-fixtures.json',
        'restaurant-fixture.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user1 = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
            )
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')
        cls.restaurant = Restaurant.objects.create(
            name='test_restaurant_for_access',
            created_by=cls.user1
            )
        cls.secure_page_url = reverse(
            'restaurantapiapp:restaurant_detail',
            args=[cls.restaurant.pk]
            )
        cls.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user1.delete()
        cls.user2.delete()
        cls.admin_user.delete()
        cls.restaurant.delete()

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {
            'username': username,
            'password': password
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # authentication test
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_for_creator_of_restaurant(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying access to restaurant details for creator of the restaurant
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['created_by'], self.user1.username)

    def test_access_for_not_creator_of_restaurant(self):
        # get token
        token = self.obtain_token('testuser2', 'testpassword2')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying deny access to restaurant details
        # for non-creator of the restaurant
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Not found.')

    def test_access_for_superuser(self):
        # get token
        token = self.obtain_token('adminuser', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying access to restaurant details
        # for superuser
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['created_by'], self.user1.username)

    def test_upgrade_restaurant(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response_old_restaurant = self.client.get(self.secure_page_url)

        data = {
            'name': 'test_restaurant_new_name',
            'location': 'test_location',
            'cuisine_type': 'test_cousine'
            }

        response_new_restaurant = self.client.put(
            self.secure_page_url,
            data=data
        )
        self.assertEqual(
            response_new_restaurant.status_code,
            status.HTTP_200_OK
            )

        response_json_old_restaurant = json.loads(
            response_old_restaurant.content
            )
        response_json_new_restaurant = json.loads(
            response_new_restaurant.content
            )

        self.assertNotEqual(
            response_json_old_restaurant['name'],
            response_json_new_restaurant['name']
            )

    def test_delete_restaurant(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_user_deny_access(self):
        # authentication test for anonymous user
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VisitsListTestCase(APITestCase):
    fixtures = [
        'user-fixtures.json',
        'restaurant-fixture.json',
        'visit-fistures.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user1 = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
            )
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')
        cls.secure_page_url = reverse('restaurantapiapp:visits_list')
        cls.restaurant1 = Restaurant.objects.create(
            name='test_restaurant_for_access1',
            created_by=cls.user1
            )
        cls.restaurant2 = Restaurant.objects.create(
            name='test_restaurant_for_access2',
            created_by=cls.user2
            )
        cls.visit = Visit.objects.create(
            date_visited='2024-01-18',
            expenses=6000,
            note='test_note2',
            rating=3,
            restaurant=cls.restaurant2
            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user1.delete()
        cls.user2.delete()
        cls.restaurant1.delete()
        cls.restaurant2.delete()
        cls.visit.delete()

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {
            'username': username,
            'password': password
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # authentication test
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_visit(self):
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # test that an authenticated user can create a visit to his restaurant
        data = {
            "date_visited": "2024-01-17",
            "expenses": 9000,
            "note": "test_note",
            "rating": 5,
            "restaurant": self.restaurant1.pk
            }
        response = self.client.post(self.secure_page_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test to see if the visit was actually created
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['results'][0]['date_visited'],
                         data['date_visited'])

        # test that the user does not have access to
        # the details of a visit he did not create
        response = self.client.get(reverse(
            'restaurantapiapp:visit_detail',
            args=[self.visit.pk]
            ))
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Not found.')

    def test_authenticated_user_cant_create_visit(self):
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # test that an authenticated user can't create
        # a visit not to his restaurant
        data = {
            "date_visited": "2024-01-17",
            "expenses": 9000,
            "note": "test_note",
            "rating": 5,
            "restaurant": self.restaurant2.pk
            }
        response = self.client.post(self.secure_page_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_user_deny_access(self):
        # authentication test for anonymous user
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VisitDetailsTestCase(APITestCase):
    fixtures = [
        'user-fixtures.json',
        'restaurant-fixture.json',
        'visit-fistures.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user1 = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
            )
        cls.login_url = reverse('restaurantapiapp:token_obtain_pair')
        cls.restaurant1 = Restaurant.objects.create(
            name='test_restaurant_for_access1',
            created_by=cls.user1
            )
        cls.restaurant2 = Restaurant.objects.create(
            name='test_restaurant_for_access2',
            created_by=cls.user2
            )
        cls.visit = Visit.objects.create(
            date_visited='2024-01-18',
            expenses=6000,
            note='test_note2',
            rating=3,
            restaurant=cls.restaurant1
            )
        cls.secure_page_url = reverse('restaurantapiapp:visit_detail',
                                      args=[cls.visit.pk])
        cls.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user1.delete()
        cls.user2.delete()
        cls.admin_user.delete()
        cls.restaurant1.delete()
        cls.restaurant2.delete()
        cls.visit.delete()

    def obtain_token(self, username, password):
        response = self.client.post(self.login_url, {
            'username': username,
            'password': password}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authentication_with_token(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # authentication test
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_for_creator_of_visit(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying access to visit details for creator of the visit
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['note'], self.visit.note)

    def test_access_for_superuser(self):
        # get token
        token = self.obtain_token('adminuser', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying access to visit details for superuser
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['note'], self.visit.note)

    def test_access_for_not_creator_of_visit(self):
        # get token
        token = self.obtain_token('testuser2', 'testpassword2')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # verifying deny access to visit details for non-creator of the visit
        response = self.client.get(self.secure_page_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Not found.')

    def test_upgrade_visit(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response_old_visit = self.client.get(self.secure_page_url)

        data = {
            "date_visited": "2024-01-17",
            "expenses": 3000,
            "note": "new_test_note",
            "rating": 5,
            "restaurant": self.restaurant1.pk
            }
        response_new_visit = self.client.put(self.secure_page_url, data=data)
        self.assertEqual(response_new_visit.status_code, status.HTTP_200_OK)

        response_json_old_visit = json.loads(response_old_visit.content)
        response_json_new_visit = json.loads(response_new_visit.content)

        self.assertNotEqual(
            response_json_old_visit['expenses'],
            response_json_new_visit['expenses']
            )

    def test_delete_visit(self):
        # get token
        token = self.obtain_token('testuser', 'testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_user_deny_access(self):
        # authentication test for anonymous user
        response = self.client.get(self.secure_page_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
