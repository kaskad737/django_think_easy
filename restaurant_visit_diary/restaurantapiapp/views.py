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
    RegisterSerializer
    )
from django.contrib.auth.models import User
from django.db.models import Avg


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
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter restaurants based on restaurants created by the current user,
        # to restrict access to non-creators
        queryset = Restaurant.objects.filter(created_by=current_user).annotate(
            _average_rating=Avg('visits__rating'),
            _average_expenses=Avg('visits__expenses')
            ).order_by('pk')

        return queryset


class RestaurantDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter restaurant details based on restaurants created by the
        # current user, to restrict access to non-creators
        queryset = Restaurant.objects.filter(created_by=current_user).annotate(
            _average_rating=Avg('visits__rating'),
            _average_expenses=Avg('visits__expenses')
            )

        return queryset


class VisitsListView(ListCreateAPIView):
    serializer_class = VisitListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter visits based on restaurants created by the current user, to
        # restrict access to non-creators
        queryset = Visit.objects.filter(restaurant__created_by=current_user)

        return queryset


class VisitDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Get the current user from the request
        current_user = self.request.user
        if current_user.is_anonymous:
            current_user = 1
        # Filter visits details based on restaurants created by the current
        # user, to restrict access to non-creators
        queryset = Visit.objects.filter(restaurant__created_by=current_user)

        return queryset
