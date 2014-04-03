import models
from wikia import api, search


class DocumentsGenerator(object):

    def __init__(self):
        super(DocumentsGenerator, self).__init__()
        self.api = api.DocumentProvider(search.WikiaSearch())

    @staticmethod
    def __check_session(session_collection):
        if len(session_collection) == 0:
            return False

        cnt = models.SessionArticle.objects.filter(session_id=session_collection[0].id).count()
        if cnt > 0:
            print models.SessionArticle.objects.filter(session_id=session_collection[0].id).delete()

        return True

    @staticmethod
    def create_document(data):
        articles = models.ArticleData.objects.filter(page_id=data['page_id'], wiki_id=data['wiki_id'])
        if len(articles) == 0:
            article = models.ArticleData(wiki_id=data['wiki_id'],
                                         page_id=data['page_id'],
                                         title=data['title'],
                                         url=data['url'])
            article.save()
            return article
        else:
            return articles[0]

    @staticmethod
    def save_article_to_session(session_id, number, article_model):
        ats_model = models.SessionArticle(session_id=session_id,
                                           article_id=article_model.id,
                                           number=number)
        ats_model.save()

    def generate_session(self, session_id):
        session = models.Session.objects.filter(id=session_id)
        if self.__check_session(session) is False:
            return False

        session_size = session[0].size
        documents = self.api.generate_new_sample(session_size, session_id)

        num = 0
        for doc in documents:
            article_model = self.create_document(doc)
            self.save_article_to_session(session_id, num, article_model)
            num += 1
