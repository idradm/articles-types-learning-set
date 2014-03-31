import models
from wikia import api


class DocumentsGenerator(object):

    api = None

    def __init__(self):
        super(DocumentsGenerator, self).__init__()
        self.api = api.DocumentProvider

    def generate_session(self, session_id):

        sesssion = models.Sessions.objects.filter(id=2)
        pass


