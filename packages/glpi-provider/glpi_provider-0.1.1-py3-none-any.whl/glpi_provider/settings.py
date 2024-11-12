import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.environ.get('GLPI_BASE_URL')
USER_TOKEN = os.environ.get('GLPI_USER_TOKEN')
STATUS = os.environ.get('TICKET_STATUS')