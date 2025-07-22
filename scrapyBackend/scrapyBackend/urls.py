from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/posts/', include('post.urls')),
    path('api/', include('scrapyBack.urls')),
    path('admin/', admin.site.urls),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/search/', include('search.urls')),
    path('api/auctions/', include('auction.urls')),
    path('api/scrap-posts/', include('scrapPosts.urls')),
    path('api/', include('recommendations.urls')),



 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)