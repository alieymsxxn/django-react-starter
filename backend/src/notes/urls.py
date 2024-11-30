from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notes.views import Notes

router = DefaultRouter()
router.register('notes', Notes)

urlpatterns = [
       path('', include(router.urls)),  # Include the router's URLs
   ]