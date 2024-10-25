from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    
    def __str__(self): 
        return f"Title: {self.title} Price: {self.price} Owner: {self.owner}"
    
class Category(models.Model):
    category = models.TextChoices(max_lenght=25)
    
    
class Bid(models.Model):
    initial_price = models.ForeignKey(AuctionListing, related_name="initial_price", on_delete=models.CASCADE, default=1)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, default=1, blank=True)
    
    def __str__(self): 
        return f"{self.initial_price} {self.current_bid}"
    
