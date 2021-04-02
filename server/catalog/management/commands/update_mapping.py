from django.core.management.base import BaseCommand, CommandError

from elasticsearch_dsl import connections


class Command(BaseCommand):
    help = 'Update a mapping on an Elasticsearch index.'

    def handle(self, *args, **options):
        index = 'wine'
        self.stdout.write(f'Update mapping on "{help}" index...')
        connection = connections.get_connection()
        if connection.indices.exists(index=index):
            connection.indices.put_mapping(index=index, body={
                'properties': {
                    'variety': {
                        'type': 'text',
                        'analyzer': 'english'
                    },
                    'winery': {
                        'type': 'text',
                        'analyzer': 'english'
                    },
                    'description': {
                        'type': 'text',
                        'analyzer': 'english'
                    }
                }
            })
            self.stdout.write(f'Updated mapping on "{index}" successfully')
        else:
            raise CommandError(f'Index "{index}" does not exist')
