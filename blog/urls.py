from django.urls import path
from .views import CategoryListCreateApiView, TagListCreateApiView, CommentListCreateApiView, BlogListCreateApiView, BlogDetailApiView


urlpatterns = [
    path('', BlogListCreateApiView.as_view()),
    path('detail/<int:pk>/', BlogDetailApiView.as_view()),
    path('tag/', TagListCreateApiView.as_view()),
    path('cat/', CategoryListCreateApiView.as_view()),
    path('comment/<int:article_id>/list-create/', CommentListCreateApiView.as_view()),
]