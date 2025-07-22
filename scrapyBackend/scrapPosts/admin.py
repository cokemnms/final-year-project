from django.contrib import admin
from .models import ScrapPost,ScrapPostAttachment,ReportedScrapPost


admin.site.register(ScrapPost)
admin.site.register(ScrapPostAttachment)

@admin.register(ReportedScrapPost)
class ReportedScrapPostAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'scrap_post', 'created_at')
    search_fields = ('reporter__email', 'scrap_post__title')
    list_filter = ('created_at',)