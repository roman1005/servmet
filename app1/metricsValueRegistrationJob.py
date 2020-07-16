from app1.models import MetricValueRegistration, Metric


def checkMetrixValueRegistration():
    ''' metric_object=Metric.objects.last()

       sample_object = MetricValueRegistration(metric=metric_object)
        sample_object.save()'''
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Metrix check", current_time)