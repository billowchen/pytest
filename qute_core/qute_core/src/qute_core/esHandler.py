from elasticsearch import Elasticsearch
from qute_core.configparserHandler import ConfigparserHandler


class EsHandler(object):

    def __init__(self, config_file, key):
        self.config = ConfigparserHandler(config_file)
        self.host = self.config.get_data(key, 'host')
        self.user = self.config.get_data(key, 'username')
        self.psw = self.config.get_data(key, 'psw')
        self.port = self.config.get_data(key, 'port')
        self.es = None
        self.connect_es()

        self.template_body = {
            "query": None,
            "sort": [],
            "from": None,
            "size": None
        }

    def connect_es(self):
        if self.user:
            self.es = Elasticsearch([self.host], http_auth=(self.user, self.psw), port=self.port)
        else:
            self.es = Elasticsearch([{'host': self.host, 'port': self.port}])

    def search(self, index, query, skip=0, size=10):
        self.template_body['query'] = query
        self.template_body['from'] = skip
        self.template_body['size'] = size

        response = self.es.search(index=index, body=self.template_body)

        total = response['hits']['total']

        return [hit['_source'] for hit in response['hits']['hits']], total
