from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('notes/save_notes/', views.save_notes, name='save_notes'),
    path('notes/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('notes/<post_id>/edit/', views.post_edit, name='post_edit'),
]
