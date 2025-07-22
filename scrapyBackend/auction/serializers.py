from rest_framework import serializers
from .models import Auction, Bid
from scrapyBack.serializers import UserSerializer  # reuse user

class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)  # ✅ show user who placed the bid

    class Meta:
        model = Bid
        fields = ['id', 'amount', 'bidder']  # ✅ show only relevant info


class AuctionSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    bids = BidSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'base_price', 'created_by', 'expires_at', 'is_active', 'max_price', 'bids', 'images', 'created_at']

    def get_images(self, obj):
        request = self.context.get('request')
        return [
            request.build_absolute_uri(image.image.url) if request else image.image.url
            for image in obj.images.all()
        ]

