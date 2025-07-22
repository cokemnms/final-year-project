from rest_framework import serializers

from scrapyBack.serializers import UserSerializer

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    auction_id = serializers.SerializerMethodField()

    def get_auction_id(self, obj):
        return obj.auction.id if obj.auction else None

    class Meta:
        model = Notification
        fields = ['id', 'body', 'type_of_notification', 'post_id', 'created_for_id']
