from django.contrib import admin

from .models import *


# List Inline Images with their related post
class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1
    extra = 1
    classes = [
        "collapse",
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline,]
    list_display = ("title", "created_at", )
    list_filter = ("title", "created_at", )
    search_fields = ("title", "text")


class FacilityInline(admin.StackedInline):
    model = Facility
    extra = 1


class ProviderInline(admin.StackedInline):
    model = Provider
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [
        FacilityInline,
        ProviderInline,
    ]
