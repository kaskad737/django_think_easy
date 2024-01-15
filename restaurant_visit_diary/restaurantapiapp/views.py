from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.db.models import Avg
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import Restaurant, Visit
from .serializers import UserSerializer, RestaurantDetailsSerializer, RestaurantListSerializer, VisitListSerializer, VisitDetailsSerializer, MyTokenObtainPairSerializer, RegisterSerializer
# from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class RestaurantsListView(ListCreateAPIView):
    queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantListSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    

class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VisitsListView(ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitListSerializer
    # permission_classes = [IsOwnerOrReadOnly]


class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailsSerializer