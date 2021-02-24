from e_commerce.celery import app
from .mailing import week_mailing


@app.task
def send_mailing():
    week_mailing()
