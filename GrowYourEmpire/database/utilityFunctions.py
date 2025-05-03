from datetime import timedelta
from django.utils import timezone
from GrowYourEmpire.models import Activity, Village

def getActivities(village):
    startDate = timezone.now()
    endDate = startDate - timedelta(days=3)
    return Activity.objects.filter(owner=village,activityDate__range=[endDate,startDate]).order_by("-activityDate")

def updateVillage(name):
    village = Village.objects.get(villageName= name)
    village.lastLogin=timezone.now()
    village.disabled=False
    village.save()