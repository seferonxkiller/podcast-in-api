from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Tag, Category, Blog, Comment


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class BlogSerializers(serializers.ModelSerializer):
    # tags_name = serializers.CharField(source='tags.title', read_only=True)
    cat_name = serializers.CharField(source='category.title', read_only=True)
    category = serializers.IntegerField(write_only=True)
    # tags_name = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializers(read_only=True, many=True)
    # def get_tags_name(self, obj):
    #     return [i.title for i in obj.tags.all()]
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'tags', 'category', 'cat_name', 'image', 'content', 'created_date']


class CommentSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username', read_only=True)
    article_name = serializers.CharField(source='article.title', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'username', 'article', 'article_name', 'content', 'created_date']

        extra_kwargs = {
            "article": {'required': False},
        }

    def create(self, validated_data):
        request = self.context['request']
        article_id = self.context['article_id']
        user_id = request.user.profile.user_id
        content = validated_data.get('content')
        instance = Comment.objects.create(article_id=article_id, user_id=user_id, content=content)
        return instance
