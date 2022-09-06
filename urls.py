from django.urls import path
from .views import HomeView, AboutView, crawl

urlpatterns = [
  path('',HomeView.as_view(), name='home'),
  path('result/', crawl, name='result'),
  path('about/',AboutView.as_view(),name='about'),
]