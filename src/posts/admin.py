from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from posts.models import Post, Category, Author, Comment, PostView

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    # list_display = [
    #     'title', 'overview', 'timestamp', 'comment_count', 'author', 'thumbnail', 
    # ]
    summernote_fields = ("content",)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostView)



