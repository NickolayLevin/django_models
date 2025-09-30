from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        sum_of_posts = (Post.objects.filter(author=self).aggregate(sum = Sum('post_rate'))['sum'] or 0) * 3
        sum_of_comments = Comment.objects.filter(user=self.user).aggregate(sum = Sum('comment_rate'))['sum']or 0
        sum_of_posts_comments = Comment.objects.filter(post__author=self).aggregate(sum = Sum('comment_rate'))['sum']or 0
        self.rating = sum_of_posts + sum_of_comments + sum_of_posts_comments
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    class PostType(models.TextChoices):
        ARTICLE = 'article', "Статья"
        NEWS = 'news', 'Новость'
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=PostType.choices, default=PostType.NEWS)
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    post_rate = models.IntegerField(default=0)

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField()

    def like(self):
        self.comment_rate += 1
        self.save()
    def dislike(self):
        self.comment_rate -= 1
        self.save()



