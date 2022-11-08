from django.urls import path, re_path, include
from .authViews import *
from . import views

app_name = 'notebook'
urlpatterns = [
    path('delete_idea/<int:pk>/', views.deleteIdeaView.as_view(), name='idea_delete'),
    path('edit_idea/<int:pk>/', views.editIdeaView.as_view(), name='idea_edit'),

    path('<int:pk>/new_idea/', views.addIdeaView.as_view(), name='idea_add'),

    #path('ideas/', views.ideasView.as_view(), name='ideas'),

    path('delete_box/<int:pk>/', views.deleteBoxView.as_view(), name='box_delete'),
    path('edit_box/<int:pk>/', views.editBoxView.as_view(), name='box_edit'),
    path('new_box/', views.addBoxView.as_view(), name='add_box'),
    path('<int:pk>/', views.boxDetailView.as_view(), name='box_detail'),
    path('', views.boxesView.as_view(), name='boxes'),

    
    path('login/', notebookLoginView.as_view(), name="login"),
    path('logout/', notebookLogoutView.as_view(), name="logout"),
    ]