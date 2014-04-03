import requests
from django.db import models
from django.contrib.auth import models as auth
from concurrent.futures import ThreadPoolExecutor


# Create your models here..
class ArticleData(models.Model):
    wikiId = models.IntegerField()
    pageId = models.IntegerField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    wikitext = models.TextField()
    html = models.TextField()

    def getData(self):
        wtr = requests.get(self.url + '?action=raw')
        if wtr.status_code == 200:
            self.wikitext = wtr.text
        hr = requests.get(self.url + '?action=render')
        if hr.status_code == 200:
            self.html = hr.text
        self.save()

    def update(self):
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.getData())

    def __unicode__(self):
        return "%d_%d" % (int(self.wikiId), int(self.pageId))


class Sessions(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField()


class State(models.Model):
    session = models.ForeignKey(Sessions)
    user = models.ForeignKey(auth.User)
    number = models.IntegerField()


class SessionArticles(models.Model):
    session = models.ForeignKey(Sessions)
    article = models.ForeignKey(ArticleData)
    number = models.IntegerField()


class Type(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    @staticmethod
    def get_in_categories():
        categories = {}
        for type in Type.objects.all():
            if type.category not in categories.keys():
                categories[str(type.category)] = []
            categories[type.category].append(str(type.name))
        return categories

    def __unicode__(self):
        return "%s:%s" % (self.category, self.name)


class ArticleTypes(models.Model):
    article = models.ForeignKey(ArticleData)
    user = models.ForeignKey(auth.User)
    changed = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type)


class Quality(models.Model):
    name = models.CharField(max_length=100)


class ArticleQuality(models.Model):
    article = models.ForeignKey(ArticleData)
    user = models.ForeignKey(auth.User)
    changed = models.DateTimeField(auto_now=True)
    quality = models.ForeignKey(Quality)


class Kind(models.Model):
    name = models.CharField(max_length=100)


class ArticleKind(models.Model):
    article = models.ForeignKey(ArticleData)
    user = models.ForeignKey(auth.User)
    changed = models.DateTimeField(auto_now=True)
    kind = models.ForeignKey(Kind)