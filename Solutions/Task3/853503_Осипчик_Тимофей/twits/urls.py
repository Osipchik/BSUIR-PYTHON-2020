from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'twits'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('<int:id>', views.twit_details),
    path('search/', views.search, name='search'),
    path('create-twit/', views.create_twit, name='create_twit'),
    path('twit/<int:id>/', views.twit_details, name='twit'),
]
