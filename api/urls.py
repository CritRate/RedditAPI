from django.urls import path
from api import views

urlpatterns = [
    path('<str:community>/', views.comment_list),
]