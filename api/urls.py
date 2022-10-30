from django.urls import path
from .views import LoginAPIView, RegisterAPIView, GetScoreAPIView, CreateArticleAPIView, ArticleListAPIView


urlpatterns = [
    path('user/register/', RegisterAPIView.as_view(),),
    path('user/login/', LoginAPIView.as_view(),),
    path('article/score/<str:pk>', GetScoreAPIView.as_view(),),
    path('article/create/', CreateArticleAPIView.as_view(),),
    path('article/list/', ArticleListAPIView.as_view()),
]