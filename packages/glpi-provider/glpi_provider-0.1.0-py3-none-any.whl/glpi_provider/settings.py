import os
from dotenv import load_dotenv


load_dotenv()

GLPI_BASE_URL = os.environ.get('GLPI_BASE_URL')
GLPI_USER_TOKEN = os.environ.get('GLPI_USER_TOKEN')
TICKET_STATUS = os.environ.get('TICKET_STATUS')