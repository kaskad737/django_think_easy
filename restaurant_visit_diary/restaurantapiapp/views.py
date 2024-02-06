from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Restaurant, Visit
from .serializers import (
    UsersListSerializer,
    RestaurantDetailsSerializer,
    RestaurantListSerializer,
    VisitListSerializer,
    VisitDetailsSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    EmailRestorePasswordSerializer,
    RestaurantsSearchSerializer,
)
from django.contrib.auth.models import User
from django.db.models import Avg
from .tasks import send_email_task
import requests


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all().order_by('pk')


class RestaurantsListView(ListCreateAPIView):
    serializer_class = RestaurantListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):

        # Get the current user from the request
        # Filter restaurants based on restaurants created by the current user,
        # to restrict access to non-creators
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 0
            queryset = Restaurant.objects.filter(
                created_by=current_user).annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            ).order_by('pk')
        elif current_user.is_superuser:
            queryset = Restaurant.objects.all().annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            ).order_by('pk')
        else:
            queryset = Restaurant.objects.filter(
                created_by=current_user).annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            ).order_by('pk')

        return queryset


class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        # Filter restaurant details based on restaurants created by the
        # current user, to restrict access to non-creators
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 0
            queryset = Restaurant.objects.filter(
                created_by=current_user).annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            )
        elif current_user.is_superuser:
            queryset = Restaurant.objects.all().annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            )
        else:
            queryset = Restaurant.objects.filter(
                created_by=current_user).annotate(
                _average_rating=Avg('visits__rating'),
                _average_expenses=Avg('visits__expenses')
            )

        return queryset


class VisitsListView(ListCreateAPIView):
    serializer_class = VisitListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        # Filter visits based on restaurants created by the current user, to
        # restrict access to non-creators
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 0
            queryset = Visit.objects.filter(
                restaurant__created_by=current_user)
        elif current_user.is_superuser:
            queryset = Visit.objects.all()
        else:
            queryset = Visit.objects.filter(
                restaurant__created_by=current_user)

        return queryset


class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        # Filter visits details based on restaurants created by the current
        # user, to restrict access to non-creators
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 0
            queryset = Visit.objects.filter(
                restaurant__created_by=current_user)
        elif current_user.is_superuser:
            queryset = Visit.objects.all()
        else:
            queryset = Visit.objects.filter(
                restaurant__created_by=current_user)

        return queryset


class EmailRestorePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailRestorePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_to_send_mail = User.objects.filter(
                email=request.data['email']
            )
            if user_to_send_mail:
                user = user_to_send_mail.values()[0]['username']
                email = request.data['email']
                # send email through celery task
                send_email_task.delay(user=user, email=email)
                return Response({'message': 'email send successfuly'})
            else:
                return Response(
                    {'message': 'there is no user with that e-mail address'}
                )

        return Response({'message': serializer.errors})


class RestaurantsSearchView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RestaurantsSearchSerializer(data=request.data)
        if serializer.is_valid():
            payload = {
                'textQuery': f'{request.data.get("search_query")}'
            }

            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': 'AIzaSyDlFBFvi9oTr5MD18vpeXxe_URmMp7ylp8',
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,'
                                    'places.websiteUri,places.rating'
            }

            url = 'https://places.googleapis.com/v1/places:searchText'

            response = requests.post(url, json=payload, headers=headers)

            if response.ok:
                response_data_list = [
                    {
                        'restaurant_name': place.get('displayName')
                        .get('text'),
                        'address': place.get('formattedAddress'),
                        'website_uri': place.get('websiteUri'),
                        'rating': place.get('rating')
                    }
                    for place in response.json()['places']
                ]

                return Response({'result': response_data_list})
            else:
                return Response({'message': response.status_code})
        else:
            return Response({'message': serializer.errors})
