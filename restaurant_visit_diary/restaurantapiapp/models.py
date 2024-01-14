from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.visit.aggregate(Avg('rating'))
    
    @property
    def average_expenses(self):
        if hasattr(self, '_average_expenses'):
            return self._average_rating
        return self.visit.aggregate(Avg('expenses'))

    def __str__(self):
        return self.name

class Visit(models.Model):
    date_visited = models.DateField()
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    restaurant = models.ForeignKey(Restaurant, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f"Visit to {self.restaurant.name} on {self.date_visited}"
