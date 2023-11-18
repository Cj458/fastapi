from dotenv import load_dotenv
from celery import Celery

from .utils import *

import redis

load_dotenv()


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

celery = Celery('worker')
celery.config_from_object('app.celeryconfig')


@celery.task
def generate_pdf_report_async(user_data, output_dir):
    return generate_pdf_report(user_data, output_dir)
