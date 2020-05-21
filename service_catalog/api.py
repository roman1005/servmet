from rest_framework import routers
from app1 import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'service', myapp_views.ServiceViewset)

