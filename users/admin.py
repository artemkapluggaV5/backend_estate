from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Agent

admin.site.register(CustomUser, UserAdmin)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'experience_years', 'rating')
