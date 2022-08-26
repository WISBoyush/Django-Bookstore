from django.urls import path

from .views import ProfileData, ProfileChangeView

urlpatterns = [
    path('info/', ProfileData.as_view(), name='profile'),
    path('<int:pk>/change/', ProfileChangeView.as_view(), name='profile_change')
]
