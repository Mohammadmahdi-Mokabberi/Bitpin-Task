from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GetScoreSerializer, LoginSerialzier, RegisterSerializer, CreateArticleSerializer
from .models import Article, UserScores

User = get_user_model()

def response_data(message=None, status_code=None, data=None):
    last_response = {}
    if message != None:
        last_response['error_message'] = message
    if status_code != None:
        last_response['status_code'] = status_code
    if data != None:
        last_response['data'] = data
    if status_code == 1:
        get_status = status.HTTP_200_OK
    else:
        get_status = status.HTTP_400_BAD_REQUEST
    return Response(last_response, status=get_status)

def get_key_error_from_serializer_errors(serializer_error):
    return [key for key in serializer_error]

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                if 'username' in fields_error:
                    return response_data(status_code=0, message='Username is invalid')
                
                if 'password1' in fields_error:
                    return response_data(status_code=0, message='Password is invalid')
                
                if 'password2' in fields_error:
                    return response_data(status_code=0, message='Repeat password is invalid')
                
                if 'password' in fields_error:
                    return response_data(status_code=0, message='The passwords are not same')
            username = request.data['username']
            password = request.data['password1']
            password = make_password(password)
            User.objects.create(username=username, password=password)
            return response_data(status_code=1, message='User Created')
        except:
            return response_data(status_code=0, message='server error')


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerialzier

    def post(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                if 'username' in fields_error:
                    return response_data(status_code=0, message='Username is invalid')
                
                if 'password' in fields_error:
                    return response_data(status_code=0, message='Password cant be empty')

            username = request.data['username']
            if not User.objects.filter(username=username).exists():
                return response_data(status_code=0, message='Username does not exist')
            user = User.objects.get(username=username)
            password = request.data['password']
            if not check_password(password, user.password):
                return response_data(status_code=0, message='Wrong Password')
            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token)
            }
            return response_data(status_code=1, data=data)
        except:
            return response_data(status_code=0, message='server error')


class CreateArticleAPIView(generics.CreateAPIView):
    serializer_class = CreateArticleSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                if 'title' in fields_error:
                    return response_data(status_code=0, message='Title is invalid')
                if 'caption' in fields_error:
                    return response_data(status_code=0, message='Capion is invalid')
            user = request.user
            title = request.data['title']
            caption = request.data['caption']
            Article.objects.create(author=user, title=title, caption=caption)
            return response_data(status_code=1, message='Article Created')
        except:
            return response_data(status_code=0, message='server error')


class ArticleListAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            qs = Article.objects.all()
            data = {}
            pointer = 1
            for article in qs:
                article_data ={
                    'title' : article.title,
                    'caption' : article.caption,
                    'article_id': article.blog_id,
                    'score_average' : article.get_score_average(),
                    'scorer_count' : article.scored_blog.count(),
                }
                if UserScores.objects.filter(article=article, user=user).exists():
                    record = UserScores.objects.get(article=article, user=user)
                    article_data['user_score'] = record.score
                data[str(pointer)] = article_data
                pointer+=1
            return response_data(status_code=1, data=data)
        except:
            return response_data(status_code=0, message='server error')


class GetScoreAPIView(generics.CreateAPIView):
    serializer_class = GetScoreSerializer
    def get_object(self):
        return self.kwargs.get('pk')

    def post(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                if 'score' in fields_error:
                    return response_data(status_code=0, message='Your score must be between 0 to 5')
            user = request.user
            score = request.data['score']
            blog_id = self.get_object()
            article = Article.objects.get(blog_id=blog_id)
            if not UserScores.objects.filter(user=user, article=article):
                UserScores.objects.create(user=user, article=article, score=score)
                article.get_score(score)
                article.save()
                return response_data(status_code=1, message='score submited')
            previous_record = UserScores.objects.get(user=user, article=article)
            previous_score = previous_record.score
            article.get_score(score - previous_score)
            previous_record.score = score
            previous_record.save()
            article.save()
            return response_data(status_code=1, message='score submited')
        except :
            return response_data(status_code=0, message='server error')