from django.urls import path
from .views import SnackListView


urlpatterns = [
    path('', SnackListView.as_view(), name="snack_list")
]