from django.urls import path
from api import views

urlpatterns = [
    path('community/', views.CreateCommunity.as_view(), name='get_post_community'),
]