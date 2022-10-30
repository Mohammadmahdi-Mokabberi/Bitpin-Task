from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model

from .utils import create_random_string

User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    blog_id = models.CharField(max_length=5)
    caption = models.CharField(max_length=1500, verbose_name='متن')
    score = models.IntegerField(default=0, db_index=True, verbose_name='جمع امتیازات')
    author = models.ForeignKey(User, related_name='article_author', on_delete=models.CASCADE, verbose_name='نویسنده')

    class Meta:
        verbose_name = 'مطلب'
        verbose_name_plural = 'مطالب'

    def get_score(self, score):
        self.score += score

    def get_score_average(self):
        scorer_count = self.scored_blog.count()
        if scorer_count == 0:
            return 0
        return self.score/scorer_count

    def save(self, *args, **kwargs):
        if self.blog_id == '':
            while True:
                blog_id = create_random_string()
                if not Article.objects.filter(blog_id=blog_id):
                    break
            self.blog_id = blog_id
        super(Article, self).save(*args, **kwargs)    


class UserScores(models.Model):
    user = models.ForeignKey(User, related_name='scorer_user', on_delete=models.CASCADE, verbose_name='امتیاز دهنده')
    article = models.ForeignKey(Article, related_name='scored_blog', on_delete=models.CASCADE, verbose_name='مطلب')
    score = models.IntegerField(default=0, verbose_name='امتیاز')

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'