from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/report/', api.report_post, name='report_post'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('comments/<uuid:pk>/delete/', api.delete_comment, name='delete_comment'),
    path('<uuid:pk>/save/', api.post_save, name='post_save'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),

    # ✅ FIXED: Correct saved posts endpoint
    path('saved/', api.get_saved_posts),
]
