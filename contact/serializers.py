from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Contact, Sub


class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'message']


class SubSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sub
        fields = ['id', 'email']
