import os

_DB_PATH = 'people_db.json'
INDEX_FILE = 'index.html'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ABSOLUTE_DB_PATH = os.path.join(DIR_PATH, _DB_PATH)
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')
ABSOLUTE_INDEX_FILE = os.path.join(TEMPLATE_PATH, INDEX_FILE)