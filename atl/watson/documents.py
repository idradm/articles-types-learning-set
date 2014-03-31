from atl.wikia import api
from atl.watson import models

class DocumentsGenerator(object):

    api = None

    def __init__(self):
        super(DocumentsGenerator, self).__init__()
        self.api = api.DocumentProvider

    def generate_session(self, session_id):
        session_model = models.Sessions()
        pass


