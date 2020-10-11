from django.contrib import admin
from .models import Post
# Register your models here.

# first method
admin.site.register(Post)

# Second method
    # @admin.register(Post)
    # class PostModelAdmin(admin.ModelAdmin):
    #     list_display=['id','title','desc']
