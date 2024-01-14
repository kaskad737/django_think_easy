from django.urls import path
from .views import (
    UsersListView,
    UserDeleteView,
    RestaurantsListView, 
    RestaurantDetailsView,
    VisitsListView,
    VisitDetailsView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'restaurantapiapp'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', UsersListView.as_view(), name='users'),
    path('user/<int:pk>/', UserDeleteView.as_view(), name='user_details'),
    path('restaurants_list/', RestaurantsListView.as_view(), name='restaurants_list'),
    path('restaurants/<int:pk>/', RestaurantDetailsView.as_view(), name='restaurant_detail'),
    path('visits_list/', VisitsListView.as_view(), name='visits_list'),
    path('visits/<int:pk>/', VisitDetailsView.as_view(), name='visit_detail'),
]