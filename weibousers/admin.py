from django.contrib import admin
from django.db import models
from django.db.models import Count
from .models import WeiboUser
from location.models import Post
from import_export.admin import ExportMixin


class PostInline(admin.TabularInline):
    model = Post
    fields = [
    	'place', 'weibo_id', 'created', 'text', 'weibo_img', 'category'
    ]
    readonly_fields = (
    	'place', 'weibo_id', 'created', 'text', 'weibo_img', 'category'
    )
    extra = 0
    can_delete = False


class WeiboUserAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['gender',]
    list_display = (
    	'weibo_name', 'weibo_id', 'gender', 'province', 'city', 
    	'location', 'post_count', 'place_count',
    )
    inlines = (PostInline,)

    def get_queryset(self, request):
    # def queryset(self, request): # For Django <1.6
        qs = super(WeiboUserAdmin, self).get_queryset(request)
        # qs = super(CustomerAdmin, self).queryset(request) # For Django <1.6
        qs = qs.annotate(Count('post'))\
        	.annotate(Count('post__place', distinct=True))
        return qs

    def post_count(self, obj):
        return obj.post__count
    post_count.admin_order_field = 'post__count'

    def place_count(self, obj):
        return obj.post__place__count
    place_count.admin_order_field = 'post__place__count'

admin.site.register(WeiboUser, WeiboUserAdmin)