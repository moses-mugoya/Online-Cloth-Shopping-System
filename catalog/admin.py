from django.contrib import admin
from .models import Category, Product, Review, Feedback


class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, AdminCategory)


class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'modified',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['modified']
admin.site.register(Product, AdminProduct)


class AdminReview(admin.ModelAdmin):
    list_display = ['user', 'created', 'modified', 'active' ]
    search_fields = ('body',)
    list_editable = ('active',)
    list_display_links = ['user']
admin.site.register(Review, AdminReview)


class AdminFeedback(admin.ModelAdmin):
    list_display = ['email', 'created']
    search_fields = ('email',)
admin.site.register(Feedback, AdminFeedback)



