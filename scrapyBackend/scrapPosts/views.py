from rest_framework import viewsets
from .models import ScrapPost
from .serializers import ScrapPostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import ScrapPost, SavedScrapPost,ScrapPostAttachment,ReportedScrapPost


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_scrap_post(request):
    serializer = ScrapPostSerializer(data=request.data)
    if serializer.is_valid():
        scrap_post = serializer.save(user=request.user)

        # Save each image in attachments
        images = request.FILES.getlist('images')
        for image in images[:5]:  # Limit to 5
            ScrapPostAttachment.objects.create(scrap_post=scrap_post, image=image)

        return Response(ScrapPostSerializer(scrap_post, context={'request': request}).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScrapPostViewSet(viewsets.ModelViewSet):
    queryset = ScrapPost.objects.all().order_by('-created_at')
    serializer_class = ScrapPostSerializer
    permission_classes = [IsAuthenticated]  # ensure only authenticated users can access

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # automatically assign user on creation

    def create(self, request, *args, **kwargs):
        data = request.data
        attachments = request.FILES.getlist('attachments')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        scrap_post = serializer.save(user=request.user)

        for file in attachments[:5]:
            ScrapPostAttachment.objects.create(scrap_post=scrap_post, image=file)

        return Response(ScrapPostSerializer(scrap_post, context={'request': request}).data)

class ScrapPostByCategoryAPIView(APIView):
    def get(self, request, category):
        posts = ScrapPost.objects.filter(category__iexact=category)
        serializer = ScrapPostSerializer(posts, many=True)
        return Response(serializer.data)
    
class GetPostsByUser(APIView):
    def get(self, request, user_id, format=None):
        posts = ScrapPost.objects.filter(user__id=user_id)  # Filter posts by user ID
        serializer = ScrapPostSerializer(posts, many=True)
        return Response(serializer.data)

    
@api_view(['GET'])
def get_posts_by_category(request, category_name):
    posts = ScrapPost.objects.filter(category__name__iexact=category_name)
    serializer = ScrapPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_scrap_post(request, pk):
    try:
        post = ScrapPost.objects.get(pk=pk)
    except ScrapPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    saved_entry = SavedScrapPost.objects.filter(user=request.user, scrap_post=post).first()

    if saved_entry:
        saved_entry.delete()
        return Response({'message': 'Post unsaved'}, status=status.HTTP_200_OK)
    else:
        SavedScrapPost.objects.create(user=request.user, scrap_post=post)
        return Response({'message': 'Post saved'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_scrap_posts(request):
    saved = ScrapPost.objects.filter(saved_by=request.user).order_by('-created_at')
    serializer = ScrapPostSerializer(saved, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_scrap_post(request, pk):
    try:
        post = ScrapPost.objects.get(pk=pk)

        # Check if the logged-in user is the owner of the post
        if post.user != request.user:
            return Response({'error': 'You are not authorized to delete this post.'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    except ScrapPost.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_scrap_post(request, pk):
    try:
        post = ScrapPost.objects.get(pk=pk)
    except ScrapPost.DoesNotExist:
        return Response({'error': 'Scrap post not found.'}, status=status.HTTP_404_NOT_FOUND)

    reason = request.data.get('reason', '')  # optional reason
    ReportedScrapPost.objects.create(
        reporter=request.user,
        scrap_post=post,
     
    )

    return Response({'message': 'Scrap post reported successfully.'}, status=status.HTTP_201_CREATED)