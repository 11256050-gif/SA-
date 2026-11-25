from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'address', 'password', 'password2', 'user_type'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': False},
            'address': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'user_type': {'required': False},
        }

    def validate(self, data):
        password2 = data.pop('password2')
        if data['password'] != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'buyer'),
        )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'address', 'bio', 'profile_picture', 'profile_picture_url',
            'user_type', 'store_name', 'is_verified', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'is_verified']

    def get_profile_picture_url(self, obj):
        if not obj.profile_picture:
            return None
        request = self.context.get('request')
        url = obj.profile_picture.url
        return request.build_absolute_uri(url) if request else url


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'bio',
            'store_name', 'profile_picture'
        ]
