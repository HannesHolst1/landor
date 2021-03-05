# -*- encoding: utf-8 -*-

from django.urls import path
from grapesjs import views

app_name = 'grapesjs'
urlpatterns = [
    path('grapesjs/<int:version>/', views.open_grapesjs, name='open_grapesjs'),

    path('pages.html', views.show_user_created_pages, name='user_created_pages'),

    path('grapesjs/<int:version>/activate/', views.activate_version, name='activate_version'),

    path('grapesjs/new/', views.create_new, name='create_new'),

    path('grapesjs/<int:version>/delete/', views.delete_version, name='delete_version'),

    # endpoint to save changes from GrapesJS
    path('grapesjs/save/', views.save_user_content, name='save_user_content'),

    # endpoint to load data into GrapesJS
    path('grapesjs/load/', views.load_user_content, name='load_user_content'),

    # endpoint to provide the user created GrapesJS-file
    path('<username>/', views.user_content, name='user_content'),

]
