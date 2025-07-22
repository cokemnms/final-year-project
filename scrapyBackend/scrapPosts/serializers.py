from .models import SavedScrapPost, ScrapPost
from rest_framework import serializers
from scrapyBack.models import User
from scrapyBack.serializers import UserSerializer
from .models import  ScrapPostAttachment



class ScrapPostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapPostAttachment
        fields = ['id', 'get_image']


class ScrapPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_saved = serializers.SerializerMethodField()
    attachments = ScrapPostAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ScrapPost
        fields = [
            'id', 'category', 'title', 'description', 'price', 'condition',
            'contact', 'delivery', 'user', 'created_at', 'is_saved', 'attachments'
        ]

        read_only_fields = ['user', 'created_at']

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False
