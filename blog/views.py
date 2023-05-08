from rest_framework import generics, permissions
from .serializers import CategorySerializers, TagSerializers, BlogSerializers, CommentSerializers
from .models import Category, Tag, Blog, Comment
from django.db.models import Q


class CategoryListCreateApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class TagListCreateApiView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class BlogListCreateApiView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        category = self.request.GET.get('category')
        tag_condition = Q()
        if tag:
            tag_condition = Q(tags__title__exact=tag)
        cat_condition = Q()
        if category:
            cat_condition = Q(category__title_exact=category)
        qs = qs.filter(tag_condition, cat_condition)
        return qs


class BlogDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        category = self.request.GET.get('category')
        tag_condition = Q()
        if tag:
            tag_condition = Q(tags__title__exact=tag)
        cat_condition = Q()
        if category:
            cat_condition = Q(category__title_exact=category)
        qs = qs.filter(tag_condition, cat_condition)
        return qs


class CommentListCreateApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        print(234)
        article_id = self.kwargs.get('article_id')
        if article_id:
            qs = qs.filter(article_id=article_id)
            return qs
        return []

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['article_id'] = self.kwargs.get('article_id')
        return ctx
