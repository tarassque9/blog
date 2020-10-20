from django.contrib import admin
from .models import User, Post, Follower
from .service import save_post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        User.objects.create_user(obj)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        save_post(obj)


admin.site.register([Follower])
