from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import MessageSerializer, MessageReadReceiptSerializer
from ..models import Message, MessageReadReceipt

# ViewSet для сообщений 
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для квитанций о прочтении сообщений
class MessageReadReceiptViewSet(viewsets.ModelViewSet):
    queryset = MessageReadReceipt.objects.all()
    serializer_class = MessageReadReceiptSerializer
    permission_classes = [IsAuthenticated]
