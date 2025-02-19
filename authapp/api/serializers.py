from rest_framework import serializers
from django.contrib.auth.models import User
from authapp.models import Profile





class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        # fields = "__all__"
        exclude=['user']



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        profile_data = self.validated_data.pop("profile")

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':'Passwords must match'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        Profile.objects.create(user=account, **profile_data)
        return account

def validate_phone_number(value):
    if len(value) < 11:
        raise serializers.ValidationError("Phone number is not valid")
    
    else:
        return value




class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)  # Username added for User model
    profile = ProfileSerializer()  # Nested Profile serializer

    class Meta:
        model = User
        fields = ['username', 'profile']

    def update(self, instance, validated_data):
        # Extract profile data
        profile_data = validated_data.pop('profile', None)

        # Update username field in User
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        # Update Profile model fields
        if profile_data:
            # Access the related Profile instance
            profile_instance = instance.profile
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()

        return instance


