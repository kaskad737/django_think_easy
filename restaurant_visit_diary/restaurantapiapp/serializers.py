from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Visit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'pk', 'username', 'password'

class RestaurantListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    average_expenses = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_average_expenses(self, obj):
        return obj.average_expenses
    
    pk = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:restaurant_detail',
    )
    class Meta:
        model = Restaurant
        fields = 'pk', 'name', 'location', 'cuisine_type', 'average_rating', 'average_expenses', 'created_by'

class RestaurantDetailsSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    average_expenses = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_average_expenses(self, obj):
        return obj.average_expenses
    
    visits = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='restaurantapiapp:visit_detail',
    )
    class Meta:
        model = Restaurant
        fields = 'pk', 'name', 'location', 'cuisine_type', 'created_by', 'visits', 'average_rating', 'average_expenses'

class VisitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant'

class VisitDetailsSerializer(serializers.ModelSerializer):
    restaurant = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:restaurant_detail',
    )
    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant'
