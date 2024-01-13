from django.urls import path
from .views import (
    RestaurantsListView, 
    RestaurantDeleteView,
    VisitsListView,
    VisitDeleteView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'restaurantapiapp'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list_restaurants/', RestaurantsListView.as_view(), name='restaurants_list'),
    path('delete_restaurants/<int:pk>/', RestaurantDeleteView.as_view(), name='restaurants_delete'),
    path('list_visits/', VisitsListView.as_view(), name='visits_list'),
    path('delete_visits/<int:pk>/', VisitDeleteView.as_view(), name='visits_delete'),
]