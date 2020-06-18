from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import path

from .views import AuthView

urlpatterns = [
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh-token', refresh_jwt_token),
    path('jwt/custom-auth', AuthView.as_view())

]
