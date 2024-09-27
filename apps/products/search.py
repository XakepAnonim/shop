# from elasticsearch_dsl import Document, Text, Keyword, Float
# from elasticsearch_dsl.connections import connections
#
# connections.create_connection(hosts=['http://127.0.0.1:9200'])
#
#
# class ProductIndex(Document):
#     uuid = Keyword()
#     name = Text()
#     description = Text()
#     price = Float()
#
#     class Index:
#         name = 'products'
