from django.contrib import admin
from .models import Place, Post, SubPlace
from import_export.admin import ExportMixin
from reversion.admin import VersionAdmin

class PlaceAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ('name', 'poiid',)

class PostAdmin(VersionAdmin):
    search_fields = ['id', 'place__name', 'sub_place__name', 'category__name']
    list_filter = ['place', 'category', 'sub_place']
    list_display = ('id', 'place', 'sub_place', 'created', 'category')
    actions = None

class SubPlaceAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ['name', 'place']
    list_display = ('name', 'poiid', 'place')
    list_filter = ['place']

    
admin.site.register(Place, PlaceAdmin)
admin.site.register(SubPlace, SubPlaceAdmin)
admin.site.register(Post, PostAdmin)