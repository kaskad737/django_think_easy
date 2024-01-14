from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.db.models import Avg

from .models import Restaurant, Visit
from .serializers import UserSerializer, RestaurantDetailsSerializer, RestaurantListSerializer, VisitListSerializer, VisitDetailsSerializer
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
    # queryset = Restaurant.objects.all()
    queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantListSerializer
    

class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    # queryset = Restaurant.objects.all()
    queryset = Restaurant.objects.all().annotate(_average_rating=Avg('visits__rating'), _average_expenses=Avg('visits__expenses'))
    serializer_class = RestaurantDetailsSerializer

class VisitsListView(ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitListSerializer
    # permission_classes = [IsCreatorOrReadOnly]

class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailsSerializer