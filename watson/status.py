from watson.models import State, Session, SessionArticle
from watson.metric import Metric
from watson.watson_exceptions import NoSessionException, NoArticlesForSessionExistsException, OutOfRangeException, SessionDoesNotExistsException


class Status():

    def __init__(self, user):
        self.metrics = {}
        state = State.objects.filter(user=user)
        if len(state) > 0:
            self.state = state[0]
        else:
            self.state = State(user=user)

    def set(self, session, number):
        number = int(max(number, 0))
        session = self.__get_session(session)
        self.state.session = session
        self.state.number = self.__validate_number(session, number)
        self.state.save()
        self.__load_metrics()
        self.__load_article_data()

    def get_current(self):
        result = {}
        for key, metric in self.metrics.items():
            current = metric.get_current()
            result[key] = current.get_value() if current else False
        return result

    def get_current_session_name(self):
        return self.state.session.name

    def get_current_number(self):
        return self.state.number

    def set_metric(self, metric, value):
        return self.metrics[metric].set(value)

    def get_url(self):
        return self.__get_session_article().article.url

    def __load_metrics(self):
        self.metrics['type'] = Metric('type', self.__get_session_article(), self.state.user)
        self.metrics['kind'] = Metric('kind', self.__get_session_article(), self.state.user)
        self.metrics['quality'] = Metric('quality', self.__get_session_article(), self.state.user)

    def __get_session(self, session):
        if session is None:
            if self.state.session_id is not None:
                return self.state.session
            else:
                sessions = Session.objects.all()[:1]
                if sessions:
                    return sessions[0]
                raise NoSessionException()
        else:
            obj = self.__load_session(session)
            if obj:
                return obj
        raise SessionDoesNotExistsException(session)

    def __get_session_article(self):
        try:
            return SessionArticle.objects.get(session=self.state.session, number=self.state.number)
        except SessionArticle.DoesNotExist:
            raise NoArticlesForSessionExistsException(self.state.session.name)

    def __load_article_data(self):
        session_article = self.__get_session_article()
        if not session_article.article.wikitext or not session_article.article.html:
            session_article.article.update()

    @staticmethod
    def __load_session(name):
        sessions = Session.objects.filter(name=name)
        return sessions[0] if len(sessions) > 0 else False

    @staticmethod
    def __validate_number(session, number):
        if 0 <= number < session.size:
            return number
        size = session.size - 1
        raise OutOfRangeException(size)
