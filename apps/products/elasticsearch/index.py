from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from apps.products.models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'filter': {
                    'remove_commas': {
                        'type': 'pattern_replace',
                        'pattern': ',',
                        'replacement': ''
                    }
                },
                'analyzer': {
                    'default': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'snowball', 'remove_commas']
                    },
                    'autocomplete': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'edge_ngram']
                    }
                }
            }
        }

    class Django:
        model = Product
        fields = [
            'uuid',
            'name',
            'image',
            'specs',
            'price',
            'priceCurrency',
            'stockQuantity',
            'isAvailable',
        ]
