from django.contrib import admin
from .models import Post, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)
    filter_horizontal = ("following",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("poster", "body", "timestamp")


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
