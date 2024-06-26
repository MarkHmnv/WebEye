import os

postgres_user = os.getenv('POSTGRES_USER', 'devuser')
postgres_password = os.getenv('POSTGRES_PASSWORD', 'changeme')
postgres_db = os.getenv('POSTGRES_DB', 'devdb')
postgres_host = os.getenv('POSTGRES_HOST', 'localhost')

redis_user = os.getenv('REDIS_USER', 'devuser')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_password = os.getenv('REDIS_PASSWORD', 'changeme')

smtp_host = os.getenv('SMTP_HOST', 'localhost')
smtp_port = os.getenv('SMTP_PORT', '587')
smtp_user = os.getenv('SMTP_USER', 'devuser')
smtp_password = os.getenv('SMTP_PASSWORD', 'changeme')