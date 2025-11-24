from rest_framework import serializers
from django.contrib.auth import get_user_model



## Serializers are used to convert data into a format that can be easily stored or transmitted.
## ModelSerializer is a shortcut for creating serializers that work with models.
    ## It automatically creates fields for all the model fields and does validation.
    ## It is a good choice when you want to create a serializer for a model.

## Serializer is a base class for all serializers.
## ModelSerializer is a subclass of Serializer.

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer): ## if you do serializers.Serializer, meta class wont work
    
    password = serializers.CharField(write_only=True)

    class Meta:
        ## Meta classes are only used with ModelSerializer. It is used to define the model and fields.
        model = User 
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

