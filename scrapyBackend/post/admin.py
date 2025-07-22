from django.contrib import admin
from .models import Post, PostAttachment, Comment
from .models import ReportedPost  # <-- NEW import

@admin.register(ReportedPost)
class ReportedPostAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'post', 'created_at')
    search_fields = ('reporter__email', 'post__title')
    list_filter = ('created_at',)

admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Comment)
