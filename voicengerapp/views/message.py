from rest_framework import viewsets
from ..serializers import MessageSerializer, MessageReadReceiptSerializer
from ..models import Message, MessageReadReceipt

# ViewSet для сообщений
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# ViewSet для квитанций о прочтении сообщений
class MessageReadReceiptViewSet(viewsets.ModelViewSet):
    queryset = MessageReadReceipt.objects.all()
    serializer_class = MessageReadReceiptSerializer
