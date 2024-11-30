from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from notes.models import Note
from django.contrib.auth import get_user_model
from console.serializers import UserSerializer

User = get_user_model()

class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['author', 'title', 'content', 'created_at', 'updated_at']
        extra_kwargs = {
                'author': {'read_only': True},
                'created_at': {'read_only': True},
                'updated_at': {'read_only': True}
                }

    def validate(self, attrs):
        request  = getattr(self.context, 'request', {})
        author  = getattr(request, 'user', User.objects.get(id=1))
        exists = Note.objects.filter(author=author, content=attrs['content'])
        if exists:
            raise ValidationError('A note with the same author and title already exists.')
        return super().validate(attrs)

    def create(self, validated_data):
        request  = getattr(self.context, 'request', {})
        author  = getattr(request, 'user', User.objects.get(id=1))
        note = Note.objects.create(author=author, **validated_data)
        return note
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
