from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import solr
from watson.models import *


class Command(BaseCommand):
    """Usage example: python manage.py importcsvtosession --session=18 --input=csv/tv_series_es_uni.csv --col=";" """
    option_list = BaseCommand.option_list + (
        make_option('-s', '--session', action='store', type='int', dest='session_id',
                    help='Sets session id to which articles are imported'),
        make_option('-i', '--input', action='store', type='string', dest='input_file',
                    help='Sets input file name (CSV file), from which articles are imported '),
        make_option('-c', '--col', action='store', type='string', dest='col',
                    help='Sets column separator, default is comma'),
        make_option('--host', action='store', type='string', dest='solr_host',
                    help='Sets solr host', default="search-s10"),
        make_option('--port', action='store', type='int', dest='solr_port',
                    help='Sets solr port', default=8983),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.solr = None

    def _handle_solr_connection(self, options):
        url = 'http://%s:%i/solr/%s'
        index_name = 'main'
        host = options.get('solr_host')
        port = options.get('solr_port')

        self.solr = solr.SolrConnection(url % (host, port, index_name))

    def handle(self, *args, **options):
        if not options['session_id'] or not options['input_file'] or not options['col']:
            raise CommandError('Command requires session id (--session=) and input file (--input=) '
                               'and separator (--col=",")')

        self._handle_solr_connection(options)

        lines_seen = set()  # holds lines already seen
        num = SessionArticle.get_max_number(options['session_id'])
        for line in open(options['input_file'], "r"):
            if line not in lines_seen:  # not a duplicate
                lines_seen.add(line)
                separator = options['col'] if options['col'] else ","
                url = line.split(separator)[1].strip()
                num += 1
                self._append_to_session(session_id=options['session_id'], article_url=url, num=num)
        session_obj = Session(id=options['session_id'])
        session_obj.size = num
        session_obj.set_autogenerate_article_set(False)
        session_obj.save(update_fields=['size'])

    def _get_article_by_url(self, url):
        query = 'url:"%s"' % url

        response = self.solr.query(q=query)

        for row in response.results:
            if 'lang' in row and 'title_'+row['lang'] in row:
                data = {
                    'wiki_id': row['wid'],
                    'page_id': row['pageid'],
                    'title': row['title_'+row['lang']],
                    'url': row['url'],
                    'article_quality': row['article_quality_i'] if 'article_quality_i' in row else 0,
                    'hub': row['hub'] if 'hub' in row else ''
                }
                print row['url']
                return data

        return None

    def _append_to_session(self, session_id, article_url, num):
        data = self._get_article_by_url(article_url)
        if data:
            article_data = ArticleData.create_from_data(data)
            SessionArticle.save_article_to_session(session_id, num, article_data.id)

