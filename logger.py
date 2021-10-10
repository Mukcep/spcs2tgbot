import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('spcs2tgbot')

logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler(f"{current_dir}/main.log", encoding='utf8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)