from rest_framework import serializers
from .models import Restaurant, Visit

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = 'pk', 'name', 'location', 'cuisine_type'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant'