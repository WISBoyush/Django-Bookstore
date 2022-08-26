from django.urls import path


from .views import (RegisterFormView,
                    UserLoginView,
                    UserLogoutView,
                    UserPasswordResetView,
                    UserPasswordResetDoneView,
                    UserPasswordResetConfirmView,
                    UserPasswordResetCompleteView)

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('non-auth/', UserLogoutView.as_view(), name='logout'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete')
]
