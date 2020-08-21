from apscheduler.schedulers.background import BackgroundScheduler


from app1.metricsValueRegistrationJob import checkMetrixValueRegistration, checkMetrixValueDeadLines
from app1.notifier import processUserNotificationQueue
from app1.models import MetricValueRegistration
job_interval=10

def start():

    scheduler = BackgroundScheduler()
    scheduler.add_job(checkMetrixValueRegistration, 'interval', seconds=job_interval)

    scheduler.add_job(checkMetrixValueDeadLines, 'interval', seconds=job_interval)

    scheduler.add_job(processUserNotificationQueue, 'interval', seconds=job_interval)
    scheduler.start()
