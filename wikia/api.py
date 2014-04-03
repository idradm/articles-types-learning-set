from random import randint


class DocumentProvider(object):

    def __init__(self, wikia_solr):
        self.data = []
        self.wikia_solr = wikia_solr

    def generate_new_sample(self, size=10, random=randint(1, 5000)):
        query = 'ns:0 AND lang:en'
        sort = 'random_%d asc' % random
        results = self.wikia_solr.query(query, 0, size, sort)

        if results is not None:
            for result in results['response']['docs']:
                item = {
                    'wiki_id': result['wid'],
                    'page_id': result['pageid'],
                    'title': result['title_' + result['lang']],
                    'url': result['url']
                }
                self.data.append(item)

        return self.data