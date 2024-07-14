from django.contrib import admin
from .models import Post, User


class PostAdmin(admin.ModelAdmin):
    list_display = ("poster", "body", "timestamp")


# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
