"""
URL configuration for alttextbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views.books import BooksView
from .views.books_bookid import BooksBookidView
from .views.books_bookid_export import BooksBookidExportView
from .views.books_bookid_images import BooksBookidImagesView
from .views.books_bookid_src import BooksBookidSrcView
from .views.images_hash import ImagesHashView

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls")),
    path("books", BooksView.as_view()),
    path("books/<str:bookId>", BooksBookidView.as_view()),
    path("books/<str:bookId>/export", BooksBookidExportView.as_view()),
    path("books/<str:bookId>/images", BooksBookidImagesView.as_view()),
    path("books/<str:bookId>/<str:src>", BooksBookidSrcView.as_view()),
    path("images/<str:hash>", ImagesHashView.as_view()),
]
