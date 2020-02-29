from django.urls import path
from api import views

urlpatterns = [
    path('community/', views.get_post_community, name='get_post_community'),
]