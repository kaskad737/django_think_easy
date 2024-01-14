from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import Restaurant, Visit
from .serializers import UserSerializer, RestaurantSerializer, VisitSerializer
from .permissions import IsCreatorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class UsersListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RestaurantsListView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class VisitsListView(ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    # permission_classes = [IsCreatorOrReadOnly]

class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer