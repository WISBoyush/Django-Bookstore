from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page_url'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='items_detail'),
    path('user/', include('users.urls')),
    path('profile/', include('profiles.urls')),

]

urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
