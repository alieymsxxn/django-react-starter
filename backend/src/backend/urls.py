from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from apis.views import CreateUserView, RetrieveUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/user/register/', CreateUserView.as_view(), name='register_user'),
    path('api/user/retrieve/', RetrieveUserView.as_view(), name='retrieve_user'),
    # path('api/', include('rest_framework.urls')),
    path('', include('notes.urls')),
]