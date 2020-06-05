from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from posts.views import (
	index, blog, post, search,
	post_create, post_update, post_delete,
    #  contact
	)
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', index),
    path('blog/', blog, name="post_list"),
    path('search/', search, name="search"),
    path('post/create/', post_create, name="post_create"),
    path('post/<id>/', post, name="post_detail"),
    path('post/<id>/update/', post_update, name="post_update"),
    path('post/<id>/delete/', post_delete, name="post_delete"),
    # path('contact/', contact, name="contact"),

    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)