from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from scrapyBack.models import User
from notification.utils import create_notification 
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def conversation_detail_or_delete(request, pk):
    try:
        conversation = Conversation.objects.get(pk=pk)
        if request.user not in conversation.users.all():
            return JsonResponse({'detail': 'Not allowed'}, status=403)

        if request.method == 'GET':
            serializer = ConversationDetailSerializer(conversation)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'DELETE':
            conversation.delete()
            return JsonResponse({'detail': 'Deleted'}, status=204)
    except Conversation.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)


@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=pk)

    sent_to = None
    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    body = request.data.get('body', '')  # text might be empty
    image = request.FILES.get('image')  # get image from request

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=body,
        image=image,
        created_by=request.user,
        sent_to=sent_to
    )

    create_notification(request, 'message_received', recipient=sent_to)

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_unread_messages(request):
    unread_exists = ConversationMessage.objects.filter(
        sent_to=request.user, is_read=False
    ).exists()
    
    return JsonResponse({'has_unread': unread_exists})

