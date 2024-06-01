import os

postgres_user = os.getenv('POSTGRES_USER', 'devuser')
postgres_password = os.getenv('POSTGRES_PASSWORD', 'changeme')
postgres_db = os.getenv('POSTGRES_DB', 'devdb')
postgres_host = os.getenv('POSTGRES_HOST', 'localhost')

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_password = os.getenv('REDIS_PASSWORD', 'changeme')