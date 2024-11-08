import os
import sys
import django

# Dynamically add the project directory to the sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_path)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


from books.models import *
from books.serializer import *

object = Book.objects.get(id=1)
serialized = BookModelSerializer(object, context={'key': 'value'})
serialized = serialized.data

serialized['title'] = 'GIVE UPON STAY'
serialized['genres'][0]['name'] = 'SON'
serialized['publisher'] = {'name': 'Mohsin Ali', 'description': 'Something'}
create = BookModelSerializer(data=serialized)
if create.is_valid():
    create.save()
serialized['title'] = 'GIVE UPON STAY'
updadte = ReviewSerializer(instance=object, data=serialized)
if updadte.is_valid():
   updadte.save()
pass

