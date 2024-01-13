from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Visit(models.Model):
    date_visited = models.DateField()
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Visit to {self.restaurant.name} on {self.date_visited}"
