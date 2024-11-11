import logging
import sys
import os
import traceback


# Настройка логов.
async def init_logging(to_console = True, filename = f'{os.path.dirname(__file__)}/logs.log'):
    if to_console and filename in [False, 'False', 'None', None, 0, '-']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO, filename=filename, filemode='w', format="%(asctime)s: %(message)s")
        if to_console:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# Сообщение в логах.
def info(message):
    logging.info(message)


# Сообщение о ошибке.
def error(message):
    logging.error(f'{message}:\n{traceback.format_exc()}')