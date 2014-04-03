class Metric():

    def __init__(self, metric, article, user):
        self.__load_model_structure(metric)
        self.session_article = article
        self.user = user

    def get_current(self):
        current = self.article_model.objects.filter(article=self.session_article.article, user=self.user)
        return current[0] if len(current) > 0 else False

    def set(self, value):
        current = self.get_current()
        if not current:
            current = self.article_model(article=self.session_article.article, user=self.user)
        current.set_value(self.__get_model(value))

    def __get_model(self, type):
        return self.model.objects.get(name=type)

    def __load_model_structure(self, metric):
        if metric == 'type':
            (self.model, self.article_model) = self.__get_type_models()
        elif metric == 'kind':
            (self.model, self.article_model) = self.__get_kind_models()
        elif metric == 'quality':
            (self.model, self.article_model) = self.__get_quality_models()

    @staticmethod
    def __get_type_models():
        from watson.models import Type, ArticleType
        return Type, ArticleType

    @staticmethod
    def __get_kind_models():
        from watson.models import Kind, ArticleKind
        return Kind, ArticleKind

    @staticmethod
    def __get_quality_models():
        from watson.models import Quality, ArticleQuality
        return Quality, ArticleQuality