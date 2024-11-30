from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from notes.models import Note
from notes.serializers import NoteSerializer

class Notes(ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [AllowAny]