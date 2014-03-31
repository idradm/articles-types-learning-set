

class DocumentProvider(object):
    wikia_solr = None
    data = []

    def __init__(self, wikia_solr):
        self.wikia_solr = wikia_solr

    def generate_new_sample(self, size=10):
        query = 'ns:0 AND lang:en'
        sort = 'random_10 asc'
        results = self.wikia_solr.query(query, 0, size, sort)
        if results is not None:
            for result in results['response']['docs']:
                item = {
                    'wiki_id': result['wid'],
                    'page_id': result['pageid'],
                    'title': result['title_'+result['lang']],
                    'url': result['url']
                }
                self.data.append(item)

        return self.data