from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ProfileAPIView, SignupAPIView, ChangePasswordAPIView,
    PublicUserAPIView, UploadAvatarAPIView
)
from .api import me, signup, get_saved_posts,report_user,reset_password,request_password_reset


urlpatterns = [
    path('me/', me, name='me'),
    path('api/signup/', SignupAPIView.as_view(), name='signup'),
    path('signup/', signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('api/saved-posts/', get_saved_posts),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('reset-password/<uid>/<token>/', reset_password, name='reset-password'),
    # ✅ Avatar Upload Route
    path('upload-avatar/', UploadAvatarAPIView.as_view(), name='upload_avatar'),
    path('users/<uuid:user_id>/report/', report_user, name='report-user')

]
