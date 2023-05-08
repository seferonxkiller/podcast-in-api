from .serializers import ContactSerializers, SubSerializers
from .models import Contact, Sub
from rest_framework import generics


class ContactListCreateApiView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializers


class SubListCreateApiView(generics.ListCreateAPIView):
    queryset = Sub.objects.all()
    serializer_class = SubSerializers

