from rest_framework import serializers
from api.hunterApi import verifyEmail, INVALID
from api.clearbitApi import enrichmentCall

from django.contrib.auth import get_user_model
User = get_user_model()


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class UserSerializerCreate(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60,
        style={'input_type': 'password', 'placeholder': 'Password'},
        write_only=True
    )
    
    first_name = serializers.CharField(max_length=60, validators=[required])
    last_name = serializers.CharField(max_length=60, validators=[required])
    
    
    class Meta:
        fields = ('email', 'password', 'first_name', 'last_name')
        model = User
    
    def validate(self, data):

        email = data['email']
        # enrichmentCall(email)
        status_code, res = verifyEmail(email)
        if status_code != 200 or 'data' not in res:
            raise serializers.ValidationError("Email validation failed with statuscode {}".format(status_code))
        if res['data']['status'] == INVALID:
            raise serializers.ValidationError("Invalid mail address")

        return data

    def create(self, validated_data):        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user