from watson import models


class Generator():

    def __init__(self, session=None, session_ids=None, metrics=None):
        self.session_name = session
        self.session_ids = session_ids
        self.metrics = metrics if metrics else []
        self.user_lower_bound = 2
        self.quality_filter = 0
        self.hub_filter = None
        self.limit = -1

    def set_metric(self, metric):
        if metric not in self.metrics:
            self.metrics.append(metric)

    def unset_metric(self, metric):
        if metric in self.metrics:
            self.metrics.remove(metric)

    def set_lower_bound(self, value):
        self.user_lower_bound = value

    def set_session(self, session):
        self.session_name = session

    def set_quality_filter(self, quality):
        self.quality_filter = quality

    def set_hub_filter(self, hub):
        self.hub_filter = hub

    def set_limit(self, limit):
        self.limit = limit

    def run(self):
        result = []
        session = False
        sessions = False

        if self.session_name is None:
            sessions = self._get_sessions()
            if sessions:
                session_articles = models.SessionArticle.objects.filter(session__in=sessions)
        else:
            session = self._get_session()
            if session:
                session_articles = models.SessionArticle.objects.filter(session=session)

        unique = []
        if session or sessions:
            for session_article in session_articles:
                if session_article.article.pk not in unique:
                    articles = models.ArticleMetrics.objects.filter(article=session_article.article)
                    result.append(self._validate_article(articles))
                    unique.append(session_article.article.pk)

        return self._serialize(result)

    def _get_session(self):
        if self.session_name is None:
            return False

        session = models.Session.objects.get(name=self.session_name)
        if self.quality_filter and session.article_quality_filter > self.quality_filter:
            return False
        if self.hub_filter and session.hub_filter and session.hub_filter != self.hub_filter:
            return False
        return session

    def _get_sessions(self):
        sessions = models.Session.objects.filter(pk__in=self.session_ids)
        return sessions

    def _serialize(self, articles):
        result = []
        for a in articles:
            if a:
                item = {
                    '_id': "%s_%s" % (a.article.wiki_id, a.article.page_id),
                    'wikiId': int(a.article.wiki_id),
                    'pageId': int(a.article.page_id),
                    'title': a.article.title,
                    'wikiText': a.article.wikitext,
                }
                for metric in self.metrics:
                    item[metric] = str(getattr(a, metric).name)
                result.append(item)
                if 0 <= self.limit <= len(result):
                    return result if self.limit else []
        return result

    def _validate_article(self, articles):
        if len(articles) < self.user_lower_bound:
            return False
        if articles[0].article.article_quality < self.quality_filter:
            return False
        if self.hub_filter and articles[0].article.hub != self.hub_filter:
            return False
        valid = set(articles)
        for metric in self.metrics:
            valid = set(self._validate_metric(articles, metric)) & valid
        valid_list = list(valid)
        return valid_list[0] if valid_list else False

    def _validate_metric(self, articles, metric):
        summary = {}
        count = 0
        value = None
        for article in articles:
            name = getattr(article, metric)
            if name is not None:
                if name not in summary:
                    summary[name] = []
                summary[name].append(article)
                if len(summary[name]) > count:
                    count = len(summary[name])
                    value = name
        if value and count >= self.user_lower_bound:
            return summary[value]
        return []
