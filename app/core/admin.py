from django.contrib import admin

from core.models import JoinIn


class JoinInAdmin(admin.ModelAdmin):
    list_display = ['slug']


admin.site.register(JoinIn, JoinInAdmin)