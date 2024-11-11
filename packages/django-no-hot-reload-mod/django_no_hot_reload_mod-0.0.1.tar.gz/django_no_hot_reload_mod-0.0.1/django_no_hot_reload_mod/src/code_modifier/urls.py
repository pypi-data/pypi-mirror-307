from django.urls import path

from . import views

urlpatterns = [
    path('code_mod/', views.code_mod, name='code_mod'),
    path('get_views_for_app/', views.get_views_for_app, name='get_views_for_app'),

]


