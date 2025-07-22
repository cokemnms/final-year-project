from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from rest_framework import serializers
from post.models import Post, PostAttachment
from .models import User,ReportedUser
from django.contrib.auth.forms import UserCreationForm 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from scrapPosts.serializers import ScrapPostSerializer
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_reset_email
from django.contrib.auth import get_user_model

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'firstName': request.user.firstName,
        'lastName': request.user.lastName,
        'email': request.user.email,
        'number': request.user.number,
        'city': request.user.city,
        'avatar': request.user.avatar.url if request.user.avatar else None,  # ✅ ADD THIS
    })

@api_view(['POST'])
@authentication_classes([])  # Allow unauthenticated users to signup
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    if User.objects.filter(email=data.get('email')).exists():
        return JsonResponse({'error': 'Email is already taken'}, status=400)

    form = SignupForm({
        'email': data.get('email'),
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'number': data.get('number'),
        'city': data.get('city'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
    else:
        message = 'error'

    return JsonResponse({'message': message})

 

# Serializers
class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'image']

class PostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'attachments']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'email', 'number','city', 'avatar']



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_posts(request):
    user = request.user
    scrap_posts = user.saved_scrap_posts.all()
    repurposed_posts = user.saved_posts.all()

    scrap_serializer = ScrapPostSerializer(scrap_posts, many=True)
    repurposed_serializer = PostSerializer(repurposed_posts, many=True, context={'request': request})

    return Response({
        'scrap_posts': scrap_serializer.data,
        'repurposed_posts': repurposed_serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_user(request, user_id):
    try:
        reported_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if reported_user == request.user:
        return Response({'error': 'You cannot report yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    if ReportedUser.objects.filter(reporter=request.user, reported_user=reported_user).exists():
        return Response({'error': 'You have already reported this user.'}, status=status.HTTP_400_BAD_REQUEST)

    ReportedUser.objects.create(
        reporter=request.user,
        reported_user=reported_user
    )

    return Response({'message': 'User reported successfully.'}, status=status.HTTP_201_CREATED)

User = get_user_model()
token_generator = PasswordResetTokenGenerator()
@api_view(['POST'])
@authentication_classes([])          # ✅ NO authentication required
@permission_classes([])              # ✅ NO permission required
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email=email)
        token = token_generator.make_token(user)
        send_reset_email(user, token)
        return Response({'message': 'Reset link sent successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=404)
    
 
@api_view(['POST'])
@authentication_classes([])  
@permission_classes([]) 
def reset_password(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=400)

        new_password = request.data.get('password')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password has been reset'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user'}, status=404)
