from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message', )

class MessageSerializer_FromTo(serializers.ModelSerializer):
    #sender = serializers.EmailField()
    #recipient = serializers.EmailField()

    class Meta:
        model = Message
        fields = ('sender', 'recipient')

    # Handle POST requests
    def to_representation(self, validated_data):
        return {
            'message': "Message from <{sender}> to <{recipient}>".format(**validated_data)
        }

class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    queryset = Message.objects.all().order_by('-pk')
    #serializer_class = MessageSerializer

    def get_serializer_class(self):
        serializers_class_map = {
            'default': MessageSerializer,
            'create': MessageSerializer_FromTo,
        }
        serializer_class = serializers_class_map.get(self.action, serializers_class_map['default'])
        print("get_serializer_class() -> %r" % serializer_class)
        return serializers_class

    # Handle POST requests differently
    def create(self, request, format=None):
        message = MessageSerializer_FromTo(data = request.data)
        if message.is_valid():
            message.save()
            return Response(message.data, status=status.HTTP_201_CREATED)
        return Response(message.errors, status=status.HTTP_400_BAD_REQUEST)
