from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        poster = request.user
        body = request.POST["new-post"]
        new_post = Post(poster=poster, body=body)
        new_post.save()

    posts = Post.objects.all().order_by("-timestamp")

    return render(request, "network/index.html", {"title": "All Posts", "posts": posts})


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, id):
    profile_user = User.objects.get(pk=id)

    is_following = (
        User.objects.get(pk=request.user.id).following.contains(profile_user)
        if request.user.is_authenticated
        else False
    )

    return render(
        request,
        "network/profile.html",
        {
            "username": profile_user.username,
            "followers": profile_user.followers.count(),
            "following": profile_user.following.count(),
            "posts": Post.objects.filter(poster=id).order_by("-timestamp"),
            "is_current_user": request.user.id == id,
            "is_following": is_following,
            "id": id,
        },
    )


@login_required
def follow(request, id):
    if request.method == "POST" and request.user.id != id:
        current_user = User.objects.get(pk=request.user.id)
        profile_user = User.objects.get(pk=id)

        if current_user.following.contains(profile_user):
            current_user.following.remove(profile_user)
        else:
            current_user.following.add(profile_user)

    return HttpResponseRedirect(reverse("profile", args=(id,)))
