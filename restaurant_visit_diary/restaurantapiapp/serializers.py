from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


from .models import Restaurant, Visit


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'pk', 'username'


class RestaurantListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    average_expenses = serializers.SerializerMethodField()
    created_by = serializers.CharField(read_only=True)

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_average_expenses(self, obj):
        return obj.average_expenses
    
    details_url = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:restaurant_detail',
        lookup_field='pk'
    )

    class Meta:
        model = Restaurant
        fields = 'pk', 'name', 'location', 'cuisine_type', 'created_by', 'average_rating', 'average_expenses', 'details_url'


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    average_expenses = serializers.SerializerMethodField()
    restaurants_list_url = serializers.SerializerMethodField()
    created_by = serializers.CharField(read_only=True)

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_average_expenses(self, obj):
        return obj.average_expenses

    def get_restaurants_list_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri('/')[:-1] + reverse('restaurantapiapp:restaurants_list')

    visits = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='restaurantapiapp:visit_detail',
    )

    class Meta:
        model = Restaurant
        fields = 'pk', 'created_by', 'name', 'location', 'cuisine_type', 'visits', 'average_rating', 'average_expenses', 'restaurants_list_url'


class VisitListSerializer(serializers.ModelSerializer):
    details_url = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:visit_detail',
        lookup_field='pk'
    )

    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant', 'details_url'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # filter restaurants in visit create only for those who created restaurant.
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            current_user = 1
        self.fields['restaurant'].queryset = Restaurant.objects.filter(created_by=current_user)


class VisitDetailsSerializer(serializers.ModelSerializer):
    visits_list_url = serializers.SerializerMethodField()

    def get_visits_list_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri('/')[:-1] + reverse('restaurantapiapp:visits_list')
    
    restaurant = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='restaurantapiapp:restaurant_detail'
    )
    
    class Meta:
        model = Visit
        fields = 'pk', 'date_visited', 'expenses', 'note', 'rating', 'restaurant', 'visits_list_url'
