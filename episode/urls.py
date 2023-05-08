from django.urls import path
from .views import EpisodeListCreateApiView, EpisodeRUDApiView, CommentListCreateApiView, LikeListCreateApiView, PlaylistListCreateAPIView, PlaylistRUDAPIView, PlaylistItemCreateAPIView

urlpatterns = [
    path('', EpisodeListCreateApiView.as_view()),
    path('detail/<int:pk>/', EpisodeRUDApiView.as_view()),
    path('comment/<int:article_id>/list-create/', CommentListCreateApiView.as_view()),
    path('like/list-create/<int:episode_id>/', LikeListCreateApiView.as_view()),

    path('playlist-list-create/', PlaylistListCreateAPIView.as_view()),
    path('playlist-rud/<int:pk>/', PlaylistRUDAPIView.as_view()),

    path('playlist/<int:playlist_id>/create/', PlaylistItemCreateAPIView.as_view()),

]