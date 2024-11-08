from django.urls import path
from books import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'book_viewset', viewset=views.BookViewSet)

urlpatterns = [
    path(route='login/', view=views.CustomLoginView.as_view(), name='c_login'),
    path(route='random/', view=views.random_view, name='randon_view'),
    path(route='api_view/', view=views.BookAPIView.as_view(), name='apiview'),
    path(route='generic_list_view/', view=views.BookListGenericView.as_view(), name='book_list_generic_view'),
    path(route='generic_create_view/', view=views.BookCreateGenericView.as_view(), name='book_create_generic_view'),
]
urlpatterns += router.urls