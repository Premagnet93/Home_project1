from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.Birthday, name='create'),
    path('list/', views.birthday_list, name='list'),
    path('<int:pk>/edit/', views.birthday_detail, name='edit'),
    path('<int:pk>/delete/', views.delete_birthday, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
