from rest_framework import serializers
from books.models import Genre
from django.contrib.auth import get_user_model
from books.models import Book, Review, Publisher


User = get_user_model()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    is_active = serializers.BooleanField(default=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    author = UserSerializer()

class GenreSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500, required=False, error_messages={
            'required': 'Please provide book description.',
            'blank': 'Description cannot be empty.',
            'max_length': 'Description cannot exceed 500 characters.'
        })

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate_name(self, name):
        if name == 'Orange':
            raise serializers.ValidationError('Ornage is prohibited as a name')
        return name

    def validate(self, attrs):
        if 'description' in attrs and attrs['description'] == 'Orange':
            raise serializers.ValidationError('Ornage is prohibited as description')
        return attrs
    

class ReviewSerializer(serializers.Serializer):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # get id
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # get str representation
    # user = serializers.StringRelatedField()
    # get specific field
    # user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    # nested serilaizer
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    rating = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance,  validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.book = validated_data.get('book', instance.book)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']
class PublisherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
class GenreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class BookModelSerializer(serializers.ModelSerializer):
    author = AuthorModelSerializer(read_only=True)
    genres = GenreModelSerializer(many=True, required=False)
    publisher = PublisherModelSerializer(write_only=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'publisher', 'genres', 'published_date']
        extra_kwargs = {
            'published_date': {'required': False},
            'title': {'error_messages': {
                'required': 'Gimme title'
            }}
        }

    def create(self, validated_data):
        return super().create(validated_data)
    def get_fields(self):
        fields = super().get_fields()
        return fields

    
    def to_internal_value(self, data):
        try:
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as exc:
            # Customize error messages
            custom_errors = {}
            for field, error_list in exc.detail.items():
                if isinstance(error_list, list):
                    # Join the list of errors into a single string
                    custom_errors[field] = ' '.join(error_list)
                else:
                    custom_errors[field] = error_list
            raise serializers.ValidationError(custom_errors)
        return validated_data

class BookHypermediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['author', 'title']