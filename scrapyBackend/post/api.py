from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Post, PostAttachment, Like, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from scrapyBack.models import User
from scrapyBack.serializers import UserSerializer
from .forms import PostForm
from notification.utils import create_notification
from .models import ReportedPost

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    form = PostForm(request.POST)
    files = request.FILES.getlist('attachments')

    if not form.is_valid():
        return JsonResponse({'error': 'Invalid post data'}, status=400)

    post = form.save(commit=False)
    post.created_by = request.user
    post.save()

    for file in files[:5]:
        attachment = PostAttachment.objects.create(image=file, created_by=request.user)
        post.attachments.add(attachment)

    post.save()
    serializer = PostSerializer(post, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    existing_like = post.likes.filter(created_by=request.user).first()

    if existing_like:
        post.likes.remove(existing_like)
        existing_like.delete()
        post.likes_count -= 1
        post.save()
        return JsonResponse({'message': 'like removed'})
    else:
        like = Like.objects.create(created_by=request.user)
        post.likes.add(like)
        post.likes_count += 1
        post.save()
        create_notification(request, 'post_like', post_id=post.id)
        return JsonResponse({'message': 'like created'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.create(
        body=request.data.get('body'),
        created_by=request.user,
        post=post
    )
    post.comments_count += 1
    post.save()

    create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    serializer = PostDetailSerializer(post, context={'request': request})
    return JsonResponse({'post': serializer.data})


# ✅ DELETE POST
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if post.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    post.delete()
    return JsonResponse({'message': 'post deleted'})


# ✅ REPORT POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_report(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    post.reported_by_users.add(request.user)
    post.save()
    return JsonResponse({'message': 'post reported'})


# ✅ SAVE / UNSAVE POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_save(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)
        return JsonResponse({'message': 'post unsaved'})
    else:
        post.saved_by.add(request.user)
        return JsonResponse({'message': 'post saved'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_posts(request):
    user = request.user
    saved_posts = Post.objects.filter(saved_by=user)
    serializer = PostSerializer(saved_posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def post_list_profile(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    posts = Post.objects.filter(created_by=user)
    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if comment.created_by != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    post = comment.post
    comment.delete()

    if post:
        post.comments_count = post.comments.count()
        post.save()

    return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    # Optional: prevent duplicate reports
    if ReportedPost.objects.filter(reporter=request.user, post=post).exists():
        return JsonResponse({'message': 'Already reported'}, status=400)

    reason = request.data.get('reason', '')
    ReportedPost.objects.create(reporter=request.user, post=post, reason=reason)
    return JsonResponse({'message': 'Post reported'})