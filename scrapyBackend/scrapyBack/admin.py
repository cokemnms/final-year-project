from django.contrib import admin
from .models import User
from .models import ReportedUser

admin.site.register(User)

@admin.register(ReportedUser)
class ReportedUserAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'created_at')
