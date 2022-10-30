from rest_framework import serializers

from api.models import Article


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    
    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']
        if password1 != password2:
            raise serializers.ValidationError({'password' : 'passwords are not same'})
        return attrs

class LoginSerialzier(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ['title', 'caption']

#class ArticleListSerializer(serializers.Serializer):



class GetScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()

    def validate(self, attrs):
        score = attrs['score']
        if score>5 or score<0:
            raise serializers.ValidationError({"score": "Your score must be between 0 to 5"})
        return attrs