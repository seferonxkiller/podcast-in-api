from django.http import JsonResponse
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Season, Episode, Comment, Like, Playlist, PlaylistItems
from .serializers import SeasonSerializers, EpisodeSerializers, CommentSerializer, LikeSerializers, \
    MiniPodcastSerializers, MiniPlaylistItemSerializers, PlaylistGetSerializers, PlaylistPostSerializers, \
    PlaylistItemGETSerializer, PlaylistItemPOSTSerializer
from rest_framework.response import Response


class EpisodeListCreateApiView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/episode/
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        category = self.request.GET.get('category')
        tag_condition = Q()
        if tag:
            tag_condition = Q(tags__title_exact=tag)
        cat_condition = Q()
        if category:
            cat_condition = Q(category__title_exact=category)
        qs = qs.filter(tag_condition, cat_condition)
        return qs


class EpisodeRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        category = self.request.GET.get('category')
        tag_condition = Q()
        if tag:
            tag_condition = Q(tags__title_exact=tag)
        cat_condition = Q()
        if category:
            cat_condition = Q(category__title_exact=category)
        qs = qs.filter(tag_condition, cat_condition)
        return qs


class CommentListCreateApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        article_id = self.kwargs.get('article_id')
        if article_id:
            qs = qs.filter(article_id=article_id)
            return qs
        return []

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['article_id'] = self.kwargs.get('article_id')
        return ctx


class LikeListCreateApiView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.profile.id
        episode_id = self.kwargs.get('episode_id')
        like = Like.objects.filter(user_id=user_id, episode_id=episode_id)
        if like:
            like.delete()
            return Response({'detail': 'Like has successfully removed from playlist'})
        obj = Like.objects.create(user_id=user_id, episode_id=episode_id)
        serializer = LikeSerializers(obj)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     print('sdfgfdsdfdsdfdsdsdssssssssssssssssss')
    #     url = request.GET.get('_url')
    #     episode = Episode.objects.get(id=url).exists()
    #     count = Like.objects.filter(user=self.request.user, episode=episode).count()
    #     # ctx = super().get_serializer_context()
    #     # ctx['episode'] = self.kwargs.get('episode')
    #     if count < 1:
    #         Like.objects.create(user=self.request.user, episode=episode)
    #         print('sddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
    #         data = {
    #                     'success': True,
    #                     'episode': episode.title,
    #                     'message': 'successfully added your wishlist'
    #                 }
    #     else:
    #         Like.objects.get(user=self.request.user, episode=episode).delete()
    #         print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    #         data = {
    #             'success': False,
    #             'episode': episode.title,
    #             'message': 'successfully removed from your wishlist'
    #         }
    #     return JsonResponse(data)


class PlaylistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistGetSerializers
        return PlaylistPostSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        author = self.request.user.profile
        if author:
            qs = qs.filter(author=author)
            return qs
        return []


class PlaylistRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistGetSerializers
        return PlaylistPostSerializers


class PlaylistItemCreateAPIView(generics.ListCreateAPIView):
    queryset = PlaylistItems.objects.all()
    serializer_class = PlaylistItemPOSTSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        music_id = self.request.data.get('music')
        playlist_id = self.kwargs.get('playlist_id')
        music = PlaylistItems.objects.filter(music_id=music_id, playlist_id=playlist_id)
        if music:
            music.delete()
            return Response({'detail': 'Music has successfully removed from playlist'})
        obj = PlaylistItems.objects.create(music_id=music_id, playlist_id=playlist_id)
        serializer = PlaylistItemGETSerializer(obj)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistItemGETSerializer
        return PlaylistItemPOSTSerializer
