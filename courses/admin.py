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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(Video)


