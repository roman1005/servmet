from django.core.mail import send_mail

from app1.models import UserNotification




def processUserNotificationQueue():
   for notfication in  UserNotification.objects.filter(status=-1, attempt__lt=10):
       notfication.delivery()

