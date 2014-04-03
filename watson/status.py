from watson.models import State, Sessions, SessionArticles, ArticleTypes, Type, ArticleQuality, Quality, ArticleKind, Kind
from watson.watson_exception import WatsonException


class Status():

    def __init__(self, user):
        try:
            self.state = State.objects.get(user=user)
        except State.DoesNotExist:
            self.state = State(user=user)

    def set(self, session, number):
        number = int(max(number, 0))
        session = self.__get_session(session)
        self.state.session = session
        self.state.number = self.__validate_number(session, number)
        self.state.save()
        self.__load_article_data()

    def get_current(self):
        article_type = self.get_current_type()
        article_quality = self.get_current_quality()
        article_kind = self.get_current_kind()
        return {
            'type': article_type.type if article_type else False,
            'quality': article_quality.quality if article_quality else False,
            'kind': article_kind.kind if article_kind else False,
        }

    def get_current_session_name(self):
        return self.state.session.name

    def get_current_number(self):
        return self.state.number

    def get_current_type(self):
        try:
            return ArticleTypes.objects.get(article=self.__get_session_article().article, user=self.state.user)
        except ArticleTypes.DoesNotExist:
            return False

    def get_current_quality(self):
        try:
            return ArticleQuality.objects.get(article=self.__get_session_article().article, user=self.state.user)
        except ArticleQuality.DoesNotExist:
            return False

    def get_current_kind(self):
        try:
            return ArticleKind.objects.get(article=self.__get_session_article().article, user=self.state.user)
        except ArticleKind.DoesNotExist:
            return False

    def set_metric(self, metric, value):
        if metric == 'type':
            self.set_type(value)
        elif metric == 'quality':
            self.set_quality(value)
        elif metric == 'kind':
            self.set_kind(value)
        else:
            raise WatsonException("Metric %s does not exists" % metric)

    def set_type(self, type):
        article_type = self.get_current_type()
        if not article_type:
            article_type = ArticleTypes(article=self.__get_session_article().article, user=self.state.user)
        article_type.type = self.__get_type_model(type)
        article_type.save()

    def set_quality(self, quality):
        article_quality = self.get_current_quality()
        if not article_quality:
            article_quality = ArticleQuality(article=self.__get_session_article().article, user=self.state.user)
        article_quality.quality = self.__get_quality_model(quality)
        article_quality.save()

    def set_kind(self, kind):
        article_kind = self.get_current_kind()
        if not article_kind:
            article_kind = ArticleKind(article=self.__get_session_article().article, user=self.state.user)
        article_kind.kind = self.__get_kind_model(kind)
        article_kind.save()

    def get_url(self):
        return self.__get_session_article().article.url

    def __get_session(self, session):
        if session is None:
            if self.state.session_id is not None:
                return self.state.session
            else:
                sessions = Sessions.objects.all()[:1]
                return sessions[0]
        else:
            obj = self.__load_session(session)
            if obj:
                return obj
        raise WatsonException("Session with %s name does not exists" % session)

    def __get_session_article(self):
        try:
            return SessionArticles.objects.get(session=self.state.session, number=self.state.number)
        except SessionArticles.DoesNotExist:
            raise WatsonException("Something went terribly wrong")

    def __load_article_data(self):
        session_article = self.__get_session_article()
        if not session_article.article.wikitext or not session_article.article.html:
            session_article.article.update()

    @staticmethod
    def __get_type_model(type):
        return Type.objects.get(name=type)

    @staticmethod
    def __get_quality_model(quality):
        return Quality.objects.get(name=quality)

    @staticmethod
    def __get_kind_model(kind):
        return Kind.objects.get(name=kind)

    @staticmethod
    def __load_session(name):
        try:
            return Sessions.objects.get(name=name)
        except Sessions.DoesNotExist:
            return False

    @staticmethod
    def __validate_number(session, number):
        if 0 <= number < session.size:
            return number
        raise WatsonException("Number out of range (current range: 0 to %d)" % session.size)
