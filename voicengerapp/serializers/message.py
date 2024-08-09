from rest_framework import serializers
from ..models import Message, MessageReadReceipt

# Сериализатор для сообщений
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        #fields = '__all__'
        exclude = ['user']

# Сериализатор для квитанций о прочтении сообщений
class MessageReadReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReadReceipt
        fields = '__all__'
