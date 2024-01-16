from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.db.models import Avg

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Restaurant, Visit
from .serializers import UserSerializer, RestaurantDetailsSerializer, RestaurantListSerializer, VisitListSerializer, VisitDetailsSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from django.contrib.auth.models import User


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class RestaurantsListView(ListCreateAPIView):
    # queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    # queryset = Restaurant.objects.filter(created_by=1).annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantListSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        # Get the current user from the request

        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter visits based on restaurants created by the current user
        queryset = Restaurant.objects.filter(created_by=current_user).annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))

        return queryset
    

class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    # queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantDetailsSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user from the request

        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter visits based on restaurants created by the current user
        queryset = Restaurant.objects.filter(created_by=current_user).annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))

        return queryset


class VisitsListView(ListCreateAPIView):
    # queryset = Visit.objects.all()
    serializer_class = VisitListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user from the request

        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter visits based on restaurants created by the current user
        queryset = Visit.objects.filter(restaurant__created_by=current_user)

        return queryset


class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailsSerializer
    # permission_classes = [IsAuthenticated]