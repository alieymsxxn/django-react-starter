# Create your tests here.
import os
import sys
import django


# Dynamically add the project directory to the sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_path)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from notes.serializers import BasicSerializer, NoteSerializer, NotesListSerializer, NoteHyperlinkedSerializer
from notes.models import Note

# note = Note.objects.get(id=1)
s = BasicSerializer(data={'name':'Mohsin Ali', 'message':'Message is this', 'custom_field': 'cUsToM'})
pass
# data = {
#     # 'author_id': 1,
#     # 'author': 'wearyMandrill6',
#     'title': 'Model Serializers 1',
#     'content': 'Model Serialziers are so coolestestest',
#     # 'created_at': '',
#     # 'updated_at': ''
# }
# note_list_serializer = NotesListSerializer(data=[data]*10)
# print(note_list_serializer)
# note_serializer = NoteSerializer(instance=note)
# print(note_serializer.is_valid())
# print(note_serializer.errors)
# print(note_serializer.save())
# print(note_serializer.data)
# print(note_serializer.validated_data)
# hyperlinked_serializer = NoteHyperlinkedSerializer(instance=note)
pass