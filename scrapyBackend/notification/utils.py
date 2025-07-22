from .models import Notification
from post.models import Post

def create_notification(request, type_of_notification, post_id=None, recipient=None):
    created_for = recipient
    body = None  # Initialize body to avoid UnboundLocalError

    if type_of_notification == 'post_like':
        body = f'{request.user.firstName} {request.user.lastName} liked one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'post_comment':
        body = f'{request.user.firstName} {request.user.lastName} commented on one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by



    else:
        # Optional: handle unexpected types, or return None to skip notification
        return None

    # Prevent self-notifications
    if created_for == request.user:
        return None  # Do not create notification

    return Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for
    )
