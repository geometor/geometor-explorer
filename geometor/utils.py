'''utils'''
import logging
import os as os

def log_init(name):
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{name}/'
    os.makedirs(out, exist_ok=True)
    filename = f'{out}/build.log'
    #  with open(filename, 'w'):
        #  pass
    print(f'log to: {filename}')

    logging.basicConfig(
            filename=filename,
            filemode='w', 
            encoding='utf-8', 
            level=logging.INFO
            )
    logging.info(f'Init {name}')

def print_log(txt=''):
    print(txt)
    logging.info(txt)

# time *********************
import datetime
from timeit import default_timer as timer

def elapsed(start_time):
    secs = timer() - start_time
    return str(datetime.timedelta(seconds=secs))
