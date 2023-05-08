from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey("profile.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    tags = models.ManyToManyField(Tag, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='blogs/', null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey("profile.Profile", on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=221, null=True, blank=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.user.get_full_name():
            return f"{self.user.user.get_full_name()}'s comment"
        return f"{self.user.user.username}'s comment"

