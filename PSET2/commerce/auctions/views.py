from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, AuctionListing, Comment, Bid


def index(request):
    category = request.GET.get("category")
    if category:
        auctions = AuctionListing.objects.filter(category=category, active=True)
    else:
        auctions = AuctionListing.objects.filter(active=True)
        
    categories = Category.objects.all().order_by("category")
    
    return render(request, "auctions/index.html",{
        "auctions": auctions,
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        ## Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        ## Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        ## Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        ## Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        photo = request.POST["photo"]
        category = request.POST["category"]
        if photo == "":
            photo = "https://imgs.search.brave.com/snFrjnmaTsGk9oDUpcYT9fZw_OkjcEk_uzI-oD46Wrg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMtbmEuc3NsLWlt/YWdlcy1hbWF6b24u/Y29tL2ltYWdlcy9J/LzcxWnlPUEg0YXlM/LmpwZw"
        
        ## Assign Category object to a variable
        if category != "":
            category_name = Category.objects.get(category=category)
        else:
            category_name = None
        
        newlisting = AuctionListing(
            title = request.POST["title"],
            description = request.POST["description"],
            price = request.POST["price"],
            photo = photo,
            category = category_name,
            owner = request.user
        )
        newlisting.save()
        
        return redirect(index)
    
    else:
        categories = Category.objects.all().order_by("category")
        return render(request, "auctions/create.html",{
            "categories": categories
        })

def auction(request, id):
    auction = AuctionListing.objects.get(id = id)
    comments = Comment.objects.all()
    
    min_price = round(auction.price +1, 2)
    
    ## Check if user is in auction watchlist. Return Bool
    watchlist = auction.watchlist.filter(id=request.user.id).exists()
    
    if request.method == "POST":
        
        ## Add or remove listing from watchlist
        if "add-watchlist" in request.POST:
            auction.watchlist.add(request.user)
        elif "remove-watchlist" in request.POST:
            auction.watchlist.remove(request.user)
            
        ## Make listing active/inactive
        if "deactivate" in request.POST:
            auction.active = False
            auction.save()
        elif "activate" in request.POST:
            auction.active = True
            auction.save()
            
        ## Add comment
        if "comment" in request.POST:
            Comment.objects.create(
                author=request.user,
                comment=request.POST["comment"],
                listing=auction)
 
        ## Add bid and update price
        if "bid" in request.POST:
            bid = Bid(bid=request.POST["bid"], user=request.user, listing=auction)
            bid.save()
            
            auction.update_price()
          
        return redirect('auction', id=auction.id)
    
    else:
        return render(request, "auctions/auction.html",{
            "auction": auction,
            "min_price": min_price,
            "watchlist": watchlist,
            "comments": comments,
            "bids": auction.bids.all(),
            "winner": auction.bids.order_by("created_at").last()
        })

def watchlist(request):
    user = request.user
    auctions = user.watchlist.all()
 
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions
    })