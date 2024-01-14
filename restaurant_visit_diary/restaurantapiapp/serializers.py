from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Visit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'pk', 'username', 'password'

class RestaurantSerializer(serializers.ModelSerializer):
    visits = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='restaurantapiapp:visit_detail',
    )
    class Meta:
        model = Restaurant
        fields = 'pk', 'name', 'location', 'cuisine_type', 'created_by', 'visits'

class VisitSerializer(serializers.ModelSerializer):
    restaurant = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:restaurant_detail',
    )
    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant'
