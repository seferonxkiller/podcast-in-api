from django.urls import path
from .views import ContactListCreateApiView, SubListCreateApiView


urlpatterns = [
    path('contact-list-create/', ContactListCreateApiView.as_view()),
    path('sub-list-create/', SubListCreateApiView.as_view()),
]