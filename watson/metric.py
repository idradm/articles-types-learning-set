import re
from watson import models


class Metrics():

    prep = re.compile(r'_([a-z])')

    def __init__(self, session_article, user):
        self.article_metrics = (models.ArticleMetrics.objects.filter(article=session_article.article, user=user).first() or
                                models.ArticleMetrics(article=session_article.article, user=user))

    def get_current(self):
        return self.article_metrics

    def toggle(self, metric, value):
        model = self._get_model(metric, value)
        if getattr(self.article_metrics, metric) == model:
            model = None
        setattr(self.article_metrics, metric, model)
        self.article_metrics.save()
        return model

    @staticmethod
    def _get_model(metric, value):
        camel_cased = Metrics.prep.sub(lambda x: x.group(1).upper(), metric.capitalize())
        return getattr(models, camel_cased).objects.get(name=value)