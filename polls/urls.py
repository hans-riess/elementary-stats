from django.urls import path
from . import views


urlpatterns = [
    path('<int:poll_id>/', views.poll_view, name='poll_view'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('',views.home, name='home'),
]