from apscheduler.schedulers.background import BackgroundScheduler
from app1.metricsValueRegistrationJob import checkMetrixValueRegistration


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(checkMetrixValueRegistration, 'interval', seconds=20)
    scheduler.start()
