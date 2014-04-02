from watson.models import State, Sessions, SessionArticles, ArticleTypes, Type
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

    def get_current_session_name(self):
        return self.state.session.name

    def get_current_number(self):
        return self.state.number

    def get_current_type(self):
        try:
            return ArticleTypes.objects.get(article=self.__get_session_article().article, user=self.state.user)
        except ArticleTypes.DoesNotExist:
            return False

    def set_type(self, type):
        article_type = self.get_current_type()
        if not article_type:
            article_type = ArticleTypes(article=self.__get_session_article().article, user=self.state.user)
        article_type.type = self.__get_type_model(type)
        article_type.save()

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
