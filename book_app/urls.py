from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='ListView'),
    path('add/', views.book_add_view, name='BookAddView'),
    path('edit/<id>',views.book_edit_view,name='editBook'),
    path('delete/<id>',views.delete,name='deleteBook'),

    path('import/',views.book_impoert_view,name='BookImportView'),
    path('import/<id>',views.book_import_to_DB,name='BookImportToDB'),
    path('api/',views.api,name='API')
]