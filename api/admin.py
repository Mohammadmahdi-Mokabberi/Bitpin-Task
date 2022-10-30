from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Article, UserScores


admin.site.register(Article,)
admin.site.register(UserScores)