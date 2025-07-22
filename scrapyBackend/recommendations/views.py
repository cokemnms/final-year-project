# recommendations/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from post.models import Post
from scrapPosts.models import ScrapPost
from post.serializers import PostSerializer
from scrapPosts.serializers import ScrapPostSerializer
from .models import UserSearch

import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user = request.user

    # Get last 5 search queries
    recent_queries = UserSearch.objects.filter(user=user).order_by('-timestamp')[:5]
    keywords = [q.query for q in recent_queries]

    post_matches = Post.objects.none()
    scrap_matches = ScrapPost.objects.none()

    for word in keywords:
        post_matches |= Post.objects.filter(body__icontains=word)
        scrap_matches |= ScrapPost.objects.filter(title__icontains=word)

    # Convert to list and shuffle
    post_list = list(post_matches.distinct())
    scrap_list = list(scrap_matches.distinct())
    random.shuffle(post_list)
    random.shuffle(scrap_list)

    posts_serialized = PostSerializer(post_list, many=True, context={'request': request})
    scraps_serialized = ScrapPostSerializer(scrap_list, many=True, context={'request': request})

    return Response({
        'crafty_posts': posts_serialized.data,
        'scrap_posts': scraps_serialized.data
    })
