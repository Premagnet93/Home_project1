from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'birthday'

urlpatterns = [
    path('', views.BirthdayCreateView.as_view(), name='create'),
    path('list/', views.BirthdayListView.as_view(), name='list'),
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
    path('login_only/', views.simple_view, name='login_only'),
    path('create/', login_required(views.BirthdayCreateView.as_view()), name='create'),
    path('create/', views.BirthdayCreateView.as_view(), name='create'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
