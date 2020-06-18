from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    categories = models.ManyToManyField(Category, related_name='movies')
    title = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.IntegerField()
    available = models.IntegerField()
    # per day
    price = models.DecimalField(decimal_places=2, max_digits=6)
    rents = models.ManyToManyField(User, through='Contract')
    active = models.BooleanField(default=True)
    register_date = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-register_date', 'id']


class Contract(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    rental_days = models.IntegerField()
