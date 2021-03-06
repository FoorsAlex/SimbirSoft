from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('notes/save_notes/', views.save_notes, name='save_notes'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('create/', views.note_create, name='note_create'),
    path('notes/<note_id>/edit/', views.note_edit, name='note_edit'),
    path('notes/<note_id>/delete/', views.note_delete, name='note_delete')
]
