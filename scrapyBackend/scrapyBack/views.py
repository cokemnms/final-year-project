from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.contrib.auth import get_user_model
from post.models import Post
from .serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView

User = get_user_model()

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def get(self, request):
        user = request.user
        posts = Post.objects.filter(created_by=user).order_by('-created_at')

        return Response({
            'user': {
                'id': str(user.id),
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'number': user.number,
                'avatar': user.avatar.url if user.avatar else None,
                'city':user.city
            },
            'posts': [
                {
                    'id': str(post.id),
                    'body': post.body,
                    'created_at': post.created_at,
                    'attachments': [a.image.url for a in post.attachments.all()]
                } for post in posts
            ]
        })

class PublicUserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=200)

class SignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        password = request.data.get("password1")
        number = request.data.get("number")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                firstName=first_name,
                lastName=last_name,
                email=email,
                password=password,
                number=number,
            )
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UploadAvatarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        avatar = request.FILES.get("avatar")
        if not avatar:
            return Response({"error": "No file provided."}, status=400)

        user.avatar = avatar
        user.save()
        return Response({"avatar_url": user.avatar.url}, status=200)

