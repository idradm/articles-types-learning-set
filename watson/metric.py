from watson import models


class Metrics():

    def __init__(self, session_article, user):
        article_metrics = models.ArticleMetrics.objects.filter(article=session_article.article, user=user)
        if len(article_metrics) > 0:
            self.article_metrics = article_metrics[0]
        else:
            self.article_metrics = models.ArticleMetrics(article=session_article.article, user=user)

    def get_current(self):
        return self.article_metrics

    def set(self, metric, value):
        model = self._get_model(metric, value)
        if getattr(self.article_metrics, metric) == model:
            model = None
        setattr(self.article_metrics, metric, model)
        self.article_metrics.save()
        return model

    @staticmethod
    def _get_model(metric, value):
        return getattr(models, metric).objects.get(name=value)