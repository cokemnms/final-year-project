from rest_framework import serializers

from scrapyBack.serializers import UserSerializer

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)  # add this


    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body','image')


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages',)

