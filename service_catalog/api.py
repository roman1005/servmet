from rest_framework import routers
from app1 import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'service_ci', myapp_views.Service_CI_Viewset)
router.register(r'staff', myapp_views.StaffViewset)
