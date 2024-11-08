from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apis.views import CreateUserView, RetrieveUserView

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Create the schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Documentation for the API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Add the schema view to your URLs
urlpatterns = [
    # your API endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name='register_user'),
    path('api/user/retrieve/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include('rest_framework.urls')),
    path('books/', include('books.urls')),
]
