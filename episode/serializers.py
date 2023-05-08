from rest_framework import serializers
from .models import Season, Episode, Comment, Like, Playlist, PlaylistItems
from blog.serializers import TagSerializers, CategorySerializers


class SeasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'season']


class EpisodeSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    category_name = serializers.CharField(source="category.title", read_only=True)
    class Meta:
        model = Episode
        fields = ['id', 'author', 'title', 'music', 'image', 'content', 'category', 'category_name', 'tags', 'views', 'season', 'created_date']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.user.username", read_only=True)
    article_name = serializers.CharField(source="article.title", read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'username', 'article', 'article_name', 'name', 'content', 'created_date']

        extra_kwargs = {
            "article": {'required': False},
        }

    def create(self, validated_data):
        request = self.context['request']
        article_id = self.context['article_id']
        author_id = request.user.profile.user_id
        content = validated_data.get('content')
        instance = Comment.objects.create(article_id=article_id, author_id=author_id, content=content)
        return instance


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'episode']


class MiniPodcastSerializers(serializers.ModelSerializer):
    author = serializers.CharField(source="author.user.username", read_only=True)
    category_name = serializers.CharField(source="category.title", read_only=True)
    tags = TagSerializers(read_only=True, many=True)
    season = serializers.CharField(source="season.season", read_only=True)

    class Meta:
        model = Episode
        fields = '__all__'


class MiniPlaylistItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = PlaylistItems
        fields = ['id', 'music']


class PlaylistGetSerializers(serializers.ModelSerializer):
    items = MiniPlaylistItemSerializers(read_only=True, many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'author', 'items']


class PlaylistPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'author']

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user.profile
        instance = super().create(validated_data)
        instance.author = author
        instance.save()
        return instance


class PlaylistItemGETSerializer(serializers.ModelSerializer):
        music = MiniPodcastSerializers(read_only=True)

        class Meta:
            model = PlaylistItems
            fields = ['id', 'music']


class PlaylistItemPOSTSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlaylistItems
            fields = ['id', 'playlist', 'music']

