from django.urls import path
from .views import index, about, post, contact

app_name = "main"
urlpatterns = [
    path('', index , name='index'),
    path('tour2/', about , name='about'),
    path('tour3/', post , name='post'),
    path('tour4/', contact , name='contact'),]
    