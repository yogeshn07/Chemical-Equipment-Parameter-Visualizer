from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv),
    path('summary/', views.latest_summary),
    path('history/', views.upload_history),
    path('report/', views.download_report),
]
