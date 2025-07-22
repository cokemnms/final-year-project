from rest_framework import serializers

from scrapyBack.serializers import UserSerializer
from scrapyBack.models import User

from .models import Post, Comment ,PostAttachment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName','lastName','avatar']


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted')

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %b %Y, %H:%M")
class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    created_at_formatted = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(created_by=request.user).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.saved_by.all()
        return False

    def get_created_at_formatted(self, obj):
        return obj.created_at.isoformat()


    class Meta:
        model = Post
        fields = (
            'id', 'title', 'body', 'likes_count', 'is_liked', 'is_saved',
            'comments_count', 'created_by', 'created_at_formatted',
            'attachments'
        )

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'body', 'likes_count', 'comments_count',
            'created_by', 'created_at_formatted',
            'attachments', 'comments'
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.isoformat()
