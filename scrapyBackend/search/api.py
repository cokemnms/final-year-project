from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from scrapyBack.models import User
from scrapyBack.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from scrapPosts.models import ScrapPost
from scrapPosts.serializers import ScrapPostSerializer

from recommendations.models import UserSearch  # ✅ NEW: Import model to store search history

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search(request):
    query = request.data.get('query', '').strip()

    if query:
        UserSearch.objects.create(user=request.user, query=query)  # ✅ NEW: Save user query

    if not query:
        return JsonResponse({'users': [], 'posts': [], 'scrap_posts': []})

    query_parts = query.split()

    if len(query_parts) == 1:
        users = User.objects.filter(
            Q(firstName__icontains=query_parts[0]) | Q(lastName__icontains=query_parts[0])
        )
    else:
        users = User.objects.filter(
            Q(firstName__icontains=query_parts[0], lastName__icontains=query_parts[-1]) |
            Q(firstName__icontains=query_parts[-1], lastName__icontains=query_parts[0])
        )

    posts = Post.objects.filter(body__icontains=query)

    scrap_posts = ScrapPost.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    return JsonResponse({
        'users': UserSerializer(users, many=True).data,
        'posts': PostSerializer(posts, many=True, context={'request': request}).data,
        'scrap_posts': ScrapPostSerializer(scrap_posts, many=True, context={'request': request}).data
    }, safe=False)
