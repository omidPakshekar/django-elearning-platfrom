from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_fiter = ['created', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'title']    

class ContentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'module', 'item', 'content_type']    

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'course', 'title']    


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Text, ItemAdmin)
admin.site.register(Image, ItemAdmin)
admin.site.register(File, ItemAdmin)
admin.site.register(Video, ItemAdmin)


