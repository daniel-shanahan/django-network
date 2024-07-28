import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        body = request.POST["new-post"].strip()

        if body == "":
            # Post body cannot be empty
            return render(
                request,
                "network/index.html",
                {
                    "title": "All Posts",
                    "posts": Post.objects.all().order_by("-timestamp"),
                    "message": "Post can not be empty.",
                },
            )

        poster = request.user
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


@login_required
def following(request):
    posts = Post.objects.filter(poster__followers=request.user.id).order_by(
        "-timestamp"
    )

    return render(
        request,
        "network/following.html",
        {"title": "Following", "posts": posts},
    )


@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether the post has been edited or liked
    if request.method == "PUT":
        data = json.loads(request.body)
        current_user = User.objects.get(pk=request.user.id)

        # Update whether the user has liked or unliked the post
        if data.get("like") is not None:
            if post.liked_by.contains(current_user):
                post.liked_by.remove(current_user)
            else:
                post.liked_by.add(current_user)

        # Update whether the poster has changed the post body
        if data.get("body") is not None:
            if current_user == post.poster:
                post.body = data["body"].strip()
            else:
                return JsonResponse(
                    {"error": "Cannot edit another user's post."}, status=403
                )

        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
