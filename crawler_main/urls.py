from django.urls import path
from .views import HomeView, AboutView, crawl
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('result/', crawl, name='result'),
  path('',HomeView.as_view(), name='home'),
  path('about/',AboutView.as_view(), name='about'),
]