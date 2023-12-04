from django.contrib import admin

from .models import Category, Comment, Location, Post


admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_display_links = ('title',)
    list_per_page = 10
    list_editable = (
        'location',
        'category',
        'is_published',
    )
    list_filter = (
        'location',
        'category',
        'is_published',
    )
    search_fields = ('title',)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'author',
        'post',
    )
    list_filter = (
        'post',
    )
    search_fields = ('text',)
    list_display_links = ('text',)
    list_per_page = 10
