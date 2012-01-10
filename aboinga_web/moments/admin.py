from django.contrib import admin
from moments.models import Caption, Moment

class CaptionInline(admin.TabularInline):
    extra = 1
    model = Caption

class MomentAdmin(admin.ModelAdmin):
    inlines = [ CaptionInline ]
    ordering = ["created_at"]
    search_fields = ['slug', 'photo']
    list_display = ['slug', 'photo', 'created_at', 'public', 'upload_ip']
admin.site.register(Moment, MomentAdmin)
