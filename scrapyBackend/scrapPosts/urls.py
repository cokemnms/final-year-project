from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScrapPostViewSet, ScrapPostByCategoryAPIView, save_scrap_post, get_saved_scrap_posts, delete_scrap_post, GetPostsByUser, report_scrap_post

router = DefaultRouter()
router.register(r'scrapposts', ScrapPostViewSet)  

urlpatterns = [
    path('', include(router.urls)),
    path('category/<str:category>/', ScrapPostByCategoryAPIView.as_view()),  
    path('<int:pk>/save/', save_scrap_post),
    path('saved-posts/', get_saved_scrap_posts),
    path('<int:pk>/delete/', delete_scrap_post),  
    path('user/<uuid:user_id>/posts/', GetPostsByUser.as_view()),  
    path('<int:pk>/report/', report_scrap_post, name='report-scrap-post'),
]
