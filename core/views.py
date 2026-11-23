
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Post, Comment, Like, Profile
from .forms import UserRegisterForm


def home(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        content = request.POST.get("content", "").strip()

        if content:
            Post.objects.create(
    author=request.user.username,
    content=content,
    image=request.FILES.get("image")
)

        return redirect("home")

    posts = Post.objects.order_by("-created_at")

    liked_post_ids = []

    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(
            user=request.user
        ).values_list("post_id", flat=True)

    return render(request, "core/home.html", {
        "posts": posts,
        "liked_post_ids": liked_post_ids
    })


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Votre compte a été créé avec succès."
            )
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "core/register.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Identifiants incorrects.")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def add_comment(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content", "").strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user.username,
                content=content
            )

    return redirect("home")


def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect("home")


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user.username
    )

    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if content:
            post.content = content
            post.save()

        return redirect("home")

    return render(request, "core/edit_post.html", {
        "post": post
    })


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user.username
    )

    if request.method == "POST":
        post.delete()

    return redirect("home")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        profile.display_name = request.POST.get(
            "display_name", ""
        ).strip()

        profile.bio = request.POST.get(
            "bio", ""
        ).strip()

        profile.city = request.POST.get(
            "city", ""
        ).strip()

        if request.FILES.get("photo"):
            profile.photo = request.FILES["photo"]

        profile.save()

        messages.success(
            request,
            "Votre profil a été mis à jour.",
            extra_tags="profile"
        )

        return redirect("profile")

    return render(request, "core/profile.html", {
        "profile": profile
    })


def public_profile(request, username):
    member = User.objects.filter(username=username).first()

    if member is None:
        messages.info(
            request,
            "Ce profil n'est pas disponible."
        )
        return redirect("home")

    profile, created = Profile.objects.get_or_create(
        user=member
    )

    posts = Post.objects.filter(
        author=member.username
    ).order_by("-created_at")

    return render(request, "core/public_profile.html", {
        "member": member,
        "profile": profile,
        "posts": posts
    })
