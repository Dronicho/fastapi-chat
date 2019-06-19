import os

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///./test.db'
DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')
