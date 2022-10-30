from django.urls import path
from .views import LoginAPIView, RegisterAPIView, GetScoreAPIView, CreateArticleAPIView, ArticleListAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(),),
    path('login/', LoginAPIView.as_view(),),
    path('score-blog/<str:pk>', GetScoreAPIView.as_view(),),
    path('create-article/', CreateArticleAPIView.as_view(),),
    path('article-list/', ArticleListAPIView.as_view()),
]