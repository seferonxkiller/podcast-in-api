from django.db import models
from blog.models import Category, Tag
from django.contrib.auth.models import User


class Season(models.Model):
    season = models.IntegerField()


class Episode(models.Model):
    author = models.ForeignKey("profile.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    music = models.FileField(upload_to='episodes/')
    image = models.ImageField(upload_to='episode_images/')
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    views = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey("profile.Profile", on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    article = models.ForeignKey(Episode, on_delete=models.CASCADE)
    name = models.CharField(max_length=221, null=True, blank=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        if self.author.user.get_full_name():
            return f"{self.author.user.get_full_name()}'s comment"
        return f"{self.author.user.username}'s comment"


class Like(models.Model):
    user = models.ForeignKey("profile.Profile", on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'{self.author.username} (id: {self.id})'


class Playlist(models.Model):
    title = models.CharField(max_length=221)
    author = models.ForeignKey("profile.Profile", on_delete=models.CASCADE, null=True)


class PlaylistItems(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, related_name='items')
    music = models.ForeignKey(Episode, on_delete=models.CASCADE)
