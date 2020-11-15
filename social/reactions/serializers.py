from rest_framework import serializers

from .models import PostReaction


class PostReactionSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostReaction
        fields = '__all__'


    def update(self, instance, validated_data):
  
        print("UPDATE")
        return instance