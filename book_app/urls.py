from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='ListView'),
    path('add/', views.BookAddView, name='BookAddView'),
    path('<pk>/edit',views.BookEditView,name='edit')
]