from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by("-timestamp")[:10]
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def create_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body")
    new_post = Post(
        user = request.user,
        body = body,
    )
    new_post.save()
    
    return JsonResponse({"status": "success"})

def user_profile(request, id):
    owner = User.objects.get(pk=id)
    posts = Post.objects.filter(user=owner).order_by("-timestamp")
    is_following = owner.following.filter(pk=request.user.id).exists()
    return render(request, "network/profile.html",{
        "owner": owner,
        "posts": posts,
        "is_following": is_following
    })

@csrf_exempt
@login_required
def following(request, id):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    is_following = user.following.filter(pk=id).exists()
    if is_following:
        user.following.remove(id)
        is_following = False
    else:
        user.following.add(id)
        is_following = True
    
    return JsonResponse({"status": "success","is_following": is_following})