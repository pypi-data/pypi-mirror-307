import logging
from ceo import get_openai_model

from tomohiro import Tomohiro

tomohiro = Tomohiro(get_openai_model())

logging.getLogger('ceo').setLevel(logging.DEBUG)

tomohiro.assign('what time is it?').just_do_it()
