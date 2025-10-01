from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)   
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']


    def create(self, attrs):
        username_exits = User.objects.filter(username=attrs['username']).exists()

        if username_exits:
            raise serializers.ValidationError( detail='User with username exits')
        
        
        email_exits = User.objects.filter(username=attrs['email']).exists()

        if email_exits:
            raise serializers.ValidationError( detail='User with email exits')
        

        phonenumber_exits = User.objects.filter(username=attrs['phone_number']).exists()

        if phonenumber_exits:
            raise serializers.ValidationError( detail='User with phonenumber exits')


        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data.get['username'],
            email = validated_data.get['email'],
            phone_number = validated_data.get['phone_number'],
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
        
        
        