from django.urls import path
from . import views

app_name = 'polls'  # This defines the namespace

urlpatterns = [
    path('<int:poll_id>/', views.poll_view, name='poll_view'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('',views.home, name='home'),
]