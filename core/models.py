
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.CharField(max_length=100, default="Membre")
    content = models.TextField()
    image = models.ImageField(
        upload_to="photos_publications/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.author}"


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} aime une publication"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField(
        upload_to="photos_profils/",
        blank=True,
        null=True
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
