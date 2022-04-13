from django.contrib import admin
from django.urls import include, path

from .views import redirectView

urlpatterns = [
    path('books/', include('book_app.urls')),
    path('admin/', admin.site.urls),
    path('',redirectView) 
]