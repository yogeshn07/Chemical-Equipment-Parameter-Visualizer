from django.urls import path
from .views import upload_csv, latest_summary, upload_history

urlpatterns = [
    path('upload/', upload_csv),
    path('summary/', latest_summary),
    path('history/', upload_history),
]
