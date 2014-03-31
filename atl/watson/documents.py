from atl.wikia import api

class DocumentsGenerator(object):

    api = None

    def __init__(self):
        super(DocumentsGenerator, self).__init__()
        self.api = api.DocumentProvider


