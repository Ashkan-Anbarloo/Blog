from django.contrib import admin
from .models import Post , Ticket , Comment , Image , Account
import os
# Register your models here.

# Inline
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class CommnetInline(admin.TabularInline):
    model = Comment
    extra = 0


# admin.site.register(post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' , 'author' , 'publish' , 'status']
    ordering = ['title' , 'publish']
    list_filter = ['status' , 'publish' , 'author']
    search_fields = ['title' , 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug' : ['title']}
    list_editable = ['status']
    # list_display_links = ['author']
    inlines = [ImageInline , CommnetInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name' , 'subject' , 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post' , 'name' , 'created' , 'active']
    list_filter = ['active' , 'created' , 'updated']
    search_fields = ['name' , 'body']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post' , 'display_title' , 'created']

    def display_title(self, obj):
        if obj.title and obj.title.strip():
            return obj.title
        if obj.image_file:
            return os.path.basename(obj.image_file.name)
        return 'No Title'

    display_title.short_description = 'title'


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user' , 'date_of_birth' , 'bio' , 'job' , 'photo']


