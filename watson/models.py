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


class SessionArticles(models.Model):
    session = models.ForeignKey(Sessions)
    article = models.ForeignKey(ArticleData)
    number = models.IntegerField()


class Type(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s:%s" % (self.category, self.name)


class ArticleTypes(models.Model):
    article = models.ForeignKey(ArticleData)
    user = models.ForeignKey(auth.User)
    changed = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type)


class State(models.Model):
    session = models.ForeignKey(Sessions)
    user = models.ForeignKey(auth.User)
    number = models.IntegerField()

    def updateState(self, session, number):
        self.session = Sessions.objects.get(name=session)
        self.number = number
        self.save()
