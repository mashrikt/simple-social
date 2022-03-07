from django.contrib import admin

from .models import Post, Reaction


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'short_description', 'created_by', 'created_at')


class ReactionAdmin(admin.ModelAdmin):
    model = Reaction
    list_display = ('id', 'type', 'created_by', 'post', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Reaction, ReactionAdmin)
