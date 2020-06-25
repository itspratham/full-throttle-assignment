from .views import UserDataView

from django.urls import path

urlpatterns = [
    path('api/',UserDataView.as_view()),
]