from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='ListView'),
    path('add/', views.BookAddView, name='BookAddView'),
    path('edit/<id>',views.BookEditView,name='editBook'),
    path('delete/<id>',views.delete,name='deleteBook'),

    path('import/',views.BookImportView,name='BookImportView'),
    path('import/<id>',views.BookImportToDB,name='BookImportToDB'),
    path('api/',views.api)
]