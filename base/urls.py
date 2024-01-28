from django.contrib import admin
from django.urls import path
from base import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('', views.index),
    path('login/', views.TokenObtainPairView.as_view()),
    path('test/', views.test), #public zone
    path('getNotes', views.getNotes), # private zone
    path('register/', views.register),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', views.products),
]
