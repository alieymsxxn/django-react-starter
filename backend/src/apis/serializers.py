from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        # fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'date_joined', 'last_modified']
        exclude = ['groups', 'user_permissions']
        read_only_fields = ['date_joined', 'last_modified', 'is_active', 'is_staff', 'last_login', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'required': False}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
