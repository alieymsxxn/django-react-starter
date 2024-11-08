from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from books.serializer import BookModelSerializer
from books.models import Book
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from books.custom_permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import Throttled
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def random_view(request):
    try:
        return Response({'message': 'Random Stuff'}, status=status.HTTP_200_OK)
    except Throttled as e:
        custom_message = 'Sike! You are being throttled.'
        return Response({'error': custom_message}, status=status.HTTP_429_TOO_MANY_REQUESTS)

class AllowAnyMixin():
    permission_classes = [AllowAny, IsOwnerOrReadOnly]

class BookAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        if request.query_params.get('id'):
            book = get_object_or_404(Book, id=request.query_params.get('id'))
        else:
            book = Book.objects.all()
        book_serializer = BookModelSerializer(instance=book, many=True)
        data = book_serializer.data
        return Response({"detail": "GET request very successful", "data": data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        book_serializer = BookModelSerializer(data=request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response({"detail": "PUT request very successful", "data": book_serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail": "PUT request failed", "data": book_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if not request.query_params.get('id'):
            return Response(  {"detail": "PUT request failed. Please provide an id"}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, id=request.query_params.get('id'))
        book_serializer = BookModelSerializer(instance=book, data=request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response({"detail": "PUT request very successful", "data": book_serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail": "PUT request failed", "data": book_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        if not request.query_params.get('id'):
            return Response({"detail": "PUT request failed. Please provide an id"}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, id=request.query_params.get('id'))
        book.delete()
        return Response({"detail": "DELETE request very successful"}, status=status.HTTP_200_OK)
    
class BookListGenericView(generics.ListAPIView, AllowAnyMixin):
    
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Example: Add custom data to the response
        custom_data = {
            'count': len(data),
            'results': data
        }
        return Response(custom_data)
    
class BookCreateGenericView(AllowAnyMixin, generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

from rest_framework.throttling import BaseThrottle
from rest_framework.response import Response
from rest_framework import status

class CustomThrottle(BaseThrottle):
    def allow_request(self, request, view):
        # Custom logic to determine if request is allowed
        return False  # Allow all requests (for example purposes)

    def wait(self):
        # Return the wait time (in seconds) before allowing the next request
        return 60  # Wait 1 minute before the next request is allowed
    def throttle_failure(self):
            # Return a custom error response
        custom_message = 'My custom response for throttling'
        return Response({'error': custom_message}, status=status.HTTP_429_TOO_MANY_REQUESTS)

from rest_framework.filters import SearchFilter, OrderingFilter
class BookViewSet(AllowAnyMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [AnonRateThrottle]
    # throttle_scope = 'book_viewset'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['id']
    # def throttled(self, request, wait):
    #     """
    #     Custom throttle response.
    #     """
    #     custom_message = 'Sike! You are being throttled.'
    #     raise Throttled(detail=custom_message)
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data

    #     # Example: Add custom data to the response
    #     custom_data = {
    #         'count': len(data),
    #         'results': data
    #     }
    #     return Response(custom_data)

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    # template_name = 'login.html'  # or any template if needed
    pass