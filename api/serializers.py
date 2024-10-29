from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Story, Contribution
import os

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id  
        representation.pop('password', None)
        representation.pop('confirm_password', None)  
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContributionSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = ['story', 'contributor', 'text', 'contributed_at']

class StorySerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    contributions = ContributionSerializer(many=True,read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'content', 'creator', 'created_at', 'is_complete', 'image', 'contributions']

    def validate_image(self, image):
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024 
        if image.size > max_size:
            raise serializers.ValidationError("Image size must not exceed 5MB.")

        # Validate file extension (only allow jpg, jpeg, png)
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension. Only .jpg, .jpeg, .png are allowed.")

        return image