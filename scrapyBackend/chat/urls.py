from django.urls import path

from . import api


urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:pk>/', api.conversation_detail_or_delete, name='conversation_detail_or_delete'),
    path('messages/unread/', api.check_unread_messages, name='check_unread_messages'),
]
