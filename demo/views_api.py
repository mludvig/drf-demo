from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message', )

class MessageSerializer_FromTo(serializers.Serializer):
    sender = serializers.EmailField(write_only = True)
    recipient = serializers.EmailField(write_only = True)
    message = serializers.CharField(read_only=True, max_length = 500)

    # Handle POST requests
    def create(self, validated_data):
        message = "Message from <{sender}> to <{recipient}>".format(**validated_data)
        return Message.objects.create(message=message)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-pk')
    serializer_class = MessageSerializer

    # Handle POST requests differently
    def create(self, request, format=None):
        message = MessageSerializer_FromTo(data = request.data)
        if message.is_valid():
            message.save()
            return Response(message.data, status=status.HTTP_201_CREATED)
        return Response(message.errors, status=status.HTTP_400_BAD_REQUEST)
