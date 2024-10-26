from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.category}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True, related_name="category_name", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    
    def __str__(self): 
        return f"ID: {self.id} Title: {self.title} Price: {self.price} Owner: {self.owner}"
    
    
class Bid(models.Model):
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing", blank=True, null=True)
    
    def __str__(self): 
        return f"{self.current_bid} {self.user}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comment = models.CharField(max_length=200)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction", null=True, blank=True)
    
    def __str__(self):
        return f"{self.author} {self.comment}"