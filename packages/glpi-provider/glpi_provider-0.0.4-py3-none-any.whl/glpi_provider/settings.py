import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.environ.get('BASE_URL')
USER_TOKEN = os.environ.get('USER_TOKEN')
TICKET_STATUS = os.environ.get('TICKET_STATUS')