from watson.models import ArticleMetrics, Type, Kind, Quality


class Metrics():

    models = {
        'type': Type,
        'kind': Kind,
        'quality': Quality,
    }

    def __init__(self, session_article, user):
        article_metrics = ArticleMetrics.objects.filter(article=session_article.article, user=user)
        if len(article_metrics) > 0:
            self.article_metrics = article_metrics[0]
        else:
            self.article_metrics = ArticleMetrics(article=session_article.article, user=user)

    def get_current(self):
        return self.article_metrics

    def set(self, metric, value):
        model = self.__get_model(metric, value)
        if getattr(self.article_metrics, metric) == model:
            model = None
        setattr(self.article_metrics, metric, model)
        self.article_metrics.save()
        return model

    def __get_model(self, metric, value):
        return self.models[metric].objects.get(name=value)