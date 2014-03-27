from django.db import models

# Create your models here.
class ArticleData(models.Model):
  wikiId = models.IntegerField()
  pageId = models.IntegerField()
  title = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  wikitext = models.TextField()
  html = models.TextField()

class Sessions(models.Model):
  name = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)

class SessionArticles(models.Model):
  session = models.ForeignKey(Sessions)
  article = models.ForeignKey(ArticleData)
  number = models.IntegerField()

class ArticleTypes(models.Model):
  article = models.ForeignKey(ArticleData)
  user = models.CharField(max_length=255)
  changed = models.DateTimeField(auto_now=True)
  type = models.CharField(max_length=100)

class State(models.Model):
  session = models.ForeignKey(Sessions)
  user = models.CharField(max_length=255)
  number = models.IntegerField()
